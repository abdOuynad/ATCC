#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import io
import re

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# ==============================================================================
# OUTILS DE LECTURE (communs aux deux fonctions)
# ==============================================================================
def _lire_lignes(filepath):
    """Lit un .xlsx ou un .csv (séparateur ';', ',' ou tabulation, avec ou sans BOM)."""
    if str(filepath).lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        ws = openpyxl.load_workbook(filepath, data_only=True).active
        return [["" if c is None else c for c in row] for row in ws.iter_rows(values_only=True)]

    with open(filepath, "r", encoding="utf-8-sig", newline="") as f:   # utf-8-sig retire le BOM
        texte = f.read()
    delim = ";" if ";" in texte else ("\t" if "\t" in texte else ",")
    return list(csv.reader(io.StringIO(texte), delimiter=delim))


def _detecter_convention(lignes):
    """
    Repère le format des nombres d'après une case qui contient à la fois ',' et '.' :
      '13,330.00'  -> 'US' (virgule = milliers, point = décimale)
      '13.330,00'  -> 'FR' (point = milliers, virgule = décimale)
    Renvoie None si aucune case ne permet de trancher.
    """
    for ligne in lignes:
        for c in ligne:
            s = str(c)
            if "," in s and "." in s and re.fullmatch(r"[\s\d.,\-]+", s):
                return "US" if s.rfind(".") > s.rfind(",") else "FR"
    return None


def _en_nombre(x, convention=None):
    """Convertit '  13,330.00 ', '75 674,815', '120,000', 13330.0, '-' ... en float (NaN si illisible)."""
    if isinstance(x, (int, float, np.integer, np.floating)):
        return float(x)
    s = str(x).strip().replace("\xa0", "").replace("\u202f", "").replace(" ", "")
    if s in ("", "-", "nan", "None"):
        return np.nan
    if convention == "US":
        s = s.replace(",", "")
    elif convention == "FR":
        s = s.replace(".", "").replace(",", ".")
    else:                                         # format inconnu : règle au cas par cas
        if "," in s and "." in s:
            if s.rfind(",") > s.rfind("."):
                s = s.replace(".", "").replace(",", ".")
            else:
                s = s.replace(",", "")
        elif s.count(",") > 1:
            s = s.replace(",", "")
        elif "," in s:
            s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return np.nan


def _zone(texte):
    """'CENTRE', 'Est', 'SUD', 'SUD 1', 'Sud2' ... -> 'CENTRE', 'EST', 'SUD', 'SUD1', 'SUD2'."""
    m = re.match(r"^\s*(CENTRE|EST|OUEST|SUD)\s*-?\s*(\d*)\s*$", str(texte), re.IGNORECASE)
    return (m.group(1).upper() + m.group(2)) if m else None


# ==============================================================================
# FONCTION 1 : Analyse et Simulation des coûts de la flotte (HALIMA2.csv)
# (ta fonction ; seules la lecture du fichier et la conversion des nombres changent,
#  repérées par "# MODIF")
# ==============================================================================
def analyser_cout_flotte_annuel(filepath_halima2):
    # MODIF : lecture robuste (CSV ; ou , / BOM / xlsx) au lieu de pd.read_csv(filepath)
    lignes = _lire_lignes(filepath_halima2)
    print("=="*40)
    print(lignes)
    print("==" * 40)
    convention = _detecter_convention(lignes)
    # covention = US
    entete = [str(c).strip() for c in lignes[0]]
    print("=="*40)
    print(entete)
    print("==" * 40)
    corps = [(list(l) + [""] * len(entete))[:len(entete)] for l in lignes[1:]]
    df = pd.DataFrame(corps, columns=entete)
    df = df.replace(r"^\s*$", np.nan, regex=True)           # cases vides -> NaN (utile pour ffill)
    df = df.rename(columns={'Année': 'Année '})              # ton code utilise 'Année ' avec espace

    manquantes = [c for c in ['Année ', 'Camion', 'Type', 'Kilométrage (Km)', 'Maintenance (DA)',
                              'Carburant (DA)', 'Documents (DA)',
                              'Masse salariale Chauffeurs (DA)'] if c not in df.columns]
    if manquantes:
        raise ValueError(f"Colonnes introuvables dans {filepath_halima2} : {manquantes}. "
                         f"Colonnes lues : {list(df.columns)}")

    df['Année '] = df['Année '].ffill()

    num_cols = [
        'Kilométrage (Km)',
        'Maintenance (DA)',
        'Carburant (DA)',
        'Documents (DA)',
        'Masse salariale Chauffeurs (DA)'
    ]

    for col in num_cols:
        # MODIF : conversion qui gère '120,000', '4,425.941', '75 674,815', '-' ...
        df[col] = df[col].map(lambda v: _en_nombre(v, convention))

    df_period = df[
        df['Année '].astype(str).str.contains(
            r'2024|2025|2026',
            na=False
        )
    ].copy()

    if df_period.empty:
        raise ValueError("Aucune donnée trouvée pour les années 2024, 2025 et 2026 dans HALIMA2.csv.")

    if df_period['Kilométrage (Km)'].isna().sum() > 0:
        median_km = df_period['Kilométrage (Km)'].median()
        df_period['Kilométrage (Km)'] = df_period['Kilométrage (Km)'].fillna(median_km)

    records = []
    for annee, group in df_period.groupby('Année '):
        group = group.copy()
        total_sal = group['Masse salariale Chauffeurs (DA)'].sum(min_count=1)
        total_km = group['Kilométrage (Km)'].sum(min_count=1)

        if pd.isna(total_sal) or total_sal == 0:
            group['Masse_Salariale_Imputee'] = 0
        else:
            if total_km > 0:
                group['Masse_Salariale_Imputee'] = (group['Kilométrage (Km)'] / total_km) * total_sal
            else:
                group['Masse_Salariale_Imputee'] = 0

        charges = [
            ('Carburant (DA)', 'Carburant_Impute'),
            ('Maintenance (DA)', 'Maintenance_Imputee'),
            ('Documents (DA)', 'Documents_Impute')
        ]

        for col_raw, col_imp in charges:
            valid = group.dropna(subset=[col_raw, 'Kilométrage (Km)'])
            valid = valid[valid['Kilométrage (Km)'] > 0]
            total_km_valid = valid['Kilométrage (Km)'].sum()

            if total_km_valid > 0:
                avg_rate = valid[col_raw].sum() / total_km_valid
            else:
                avg_rate = 0

            group[col_imp] = group[col_raw].where(
                group[col_raw].notna(),
                group['Kilométrage (Km)'] * avg_rate
            )

        records.append(group)

    df_clean = pd.concat(records, ignore_index=True)

    summary = (
        df_clean
        .groupby(['Camion', 'Type'], dropna=False)
        .agg(
            Somme_Km_3ans=('Kilométrage (Km)', 'sum'),
            Somme_Maint_3ans=('Maintenance_Imputee', 'sum'),
            Somme_Carb_3ans=('Carburant_Impute', 'sum'),
            Somme_Doc_3ans=('Documents_Impute', 'sum'),
            Somme_Sal_3ans=('Masse_Salariale_Imputee', 'sum')
        )
        .reset_index()
    )

    summary['Somme_Depenses_3ans'] = (
        summary['Somme_Maint_3ans']
        + summary['Somme_Carb_3ans']
        + summary['Somme_Doc_3ans']
        + summary['Somme_Sal_3ans']
    )

    summary['Km_Moyen_An'] = summary['Somme_Km_3ans'] / 3.0
    summary['Maint_Moyenne_An'] = summary['Somme_Maint_3ans'] / 3.0
    summary['Carb_Moyenne_An'] = summary['Somme_Carb_3ans'] / 3.0
    summary['Doc_Moyen_An'] = summary['Somme_Doc_3ans'] / 3.0
    summary['Sal_Moyen_An'] = summary['Somme_Sal_3ans'] / 3.0
    summary['Depenses_Moyennes_An'] = summary['Somme_Depenses_3ans'] / 3.0

    summary['Cout_Revient_DA_Km'] = np.where(
        summary['Km_Moyen_An'] > 0,
        summary['Depenses_Moyennes_An'] / summary['Km_Moyen_An'],
        np.nan
    )

    cols_finales = [
        'Camion', 'Type', 'Km_Moyen_An', 'Maint_Moyenne_An',
        'Carb_Moyenne_An', 'Doc_Moyen_An', 'Sal_Moyen_An',
        'Depenses_Moyennes_An', 'Cout_Revient_DA_Km'
    ]

    return summary[cols_finales]


# ==============================================================================
# FONCTION 2 : Analyse et simulation des tarifs par zone (HALIMA.csv ou .xlsx)
# ==============================================================================
def regresser_tarif_par_zone():
    #lignes = _lire_lignes("./app/code/HALIMA2.csv")
    lignes = _lire_lignes("HALIMA.csv")
    convention = _detecter_convention(lignes)

    rows, zone = [], None
    for ligne in lignes:
        if not ligne or not any(str(c).strip() for c in ligne):
            continue
        first = str(ligne[0]).strip()
        z = _zone(first)
        if z:                                   # ligne "CENTRE", "EST", "SUD 1" ...
            zone = z
            continue
        if first.lower() in ("wilayas", "wilaya"):
            continue
        if zone and first and len(ligne) >= 7:
            cellules = list(ligne[1:11])
            cellules += [""] * (10 - len(cellules))      # complète si la ligne est courte
            rows.append([zone, first] + cellules)

    cols = ['Zone', 'Wilaya', 'fourgonnette', 'Fourgon_1T5', 'Fourgon_2T5',
            'Camion_3T5', 'Camion_5T_10T', 'Camion_20T', 'Km', 'Temps', 'Meteo', 'Etat_Route']
    df = pd.DataFrame(rows, columns=cols)

    # --- contrôles : on s'arrête avec un message clair plutôt que de continuer à vide ---
    if df.empty:
        raise ValueError("Aucune ligne de trajet lue dans le fichier. "
                         f"Premières lignes lues : {lignes[:3]!r}")
    brut_exemple = df['fourgonnette'].head(3).tolist()

    num_cols = ['fourgonnette', 'Fourgon_1T5', 'Fourgon_2T5', 'Camion_3T5',
                'Camion_5T_10T', 'Camion_20T', 'Km', 'Meteo', 'Etat_Route']
    for col in num_cols:
        df[col] = df[col].map(lambda v: _en_nombre(v, convention))

    if df['fourgonnette'].notna().sum() == 0 or df['Km'].notna().sum() == 0:
        raise ValueError("Prix ou km illisibles après conversion. "
                         f"Exemples de valeurs brutes de 'fourgonnette' : {brut_exemple!r}")

    zones = list(dict.fromkeys(df['Zone']))          # zones dans l'ordre du fichier
    veh_cols = ['Fourgon_1T5', 'Fourgon_2T5', 'Camion_3T5', 'Camion_5T_10T', 'Camion_20T']

    # Étape 1 : régression par zone sur les trajets OBSERVÉS uniquement
    obs = df[df['Km'].notna() & df['fourgonnette'].notna()]
    models_dict, reg_results = {}, []
    for zone in zones:
        grp = obs[obs['Zone'] == zone]
        if len(grp) < 2:                              # pas assez de points pour une droite
            continue
        X, y = grp[['Km']].values, grp['fourgonnette'].values
        model = LinearRegression().fit(X, y)
        models_dict[zone] = model
        a, b = float(model.intercept_), float(model.coef_[0])
        mape = float(np.mean(np.abs(model.predict(X) - y) / y) * 100)
        reg_results.append({
            'Zone': zone,
            'Nombre_Trajets': len(grp),
            'Frais_Fixe_a_DA': round(a, 2),
            'Tarif_Km_b_DA': round(b, 2),
            'R2': round(model.score(X, y), 4),
            'Erreur_moy_%': round(mape, 1),
            'Equation': f"T_base = {a:.2f} + {b:.2f} * Km",
        })
    df_regres = pd.DataFrame(reg_results)

    # Étape 2 : simulation des tarifs 'fourgonnette' manquants (repérés dans une colonne)
    df['fourgonnette_simulee'] = False
    for zone, model in models_dict.items():
        masque = (df['Zone'] == zone) & df['fourgonnette'].isna() & df['Km'].notna()
        if masque.any():
            df.loc[masque, 'fourgonnette'] = model.predict(df.loc[masque, ['Km']].values)
            df.loc[masque, 'fourgonnette_simulee'] = True

    # Étape 3 : ratios réels par rapport à la fourgonnette (trajets observés uniquement)
    ratios = {}
    for col in veh_cols:
        sous = obs.dropna(subset=[col])
        sous = sous[sous['fourgonnette'] > 0]
        if sous.empty:                                # plus de valeur par défaut silencieuse
            raise ValueError(f"Impossible de calculer le ratio de {col} : "
                             "aucune ligne avec les deux prix lisibles.")
        ratios[col] = float((sous[col] / sous['fourgonnette']).mean())

    # Étape 4 : simulation des autres véhicules si leurs cases sont vides
    for col in veh_cols:
        masque = df[col].isna() & df['fourgonnette'].notna()
        df.loc[masque, col] = df.loc[masque, 'fourgonnette'] * ratios[col]

    ratios_vehicules = {'fourgonnette': 1.0}
    for col in veh_cols:
        ratios_vehicules[col] = round(ratios[col], 2)

    return df_regres, models_dict, ratios_vehicules, df


# ==============================================================================
# SCRIPT PRINCIPAL D'EXÉCUTION
# ==============================================================================
if __name__ == "__main__":

    print("=" * 80)
    print("ANALYSE ET SIMULATION ANNUELLE DES COÛTS DE LA FLOTTE (HALIMA2.csv)")
    print("=" * 80)
    try:
        df_couts = analyser_cout_flotte_annuel("HALIMA3.csv")
        print(df_couts.to_string(index=False, float_format='{:,.2f}'.format))
        df_couts.to_csv("resultats_cout_flotte_annuel.csv", index=False, encoding="utf-8-sig")
        print("\n-> Résultats enregistrés dans 'resultats_cout_flotte_annuel.csv'.\n")
    except FileNotFoundError:
        print("Fichier 'HALIMA2.csv' non trouvé.\n")

    print("=" * 80)
    print("ANALYSE ET SIMULATION DES TARIFS PAR ZONE (HALIMA.csv)")
    print("=" * 80)

    try:
        df_reg, models, ratios, df_clean = regresser_tarif_par_zone()
        print(df_reg.to_string(index=False))
        df_reg.to_csv("resultats_regression_zones.csv", index=False, encoding="utf-8-sig")

        print("\n" + "-" * 50)
        print("COEFFICIENTS MULTIPLICATEURS PAR TYPE DE VÉHICULE :")
        print("-" * 50)
        for veh, ratio in ratios.items():
            print(f"  • {veh:15s} : x{ratio:.2f}")

    except FileNotFoundError:
        print("Fichier 'HALIMA.csv' non trouvé.")


def calculer_coeff_difficulte(
    meteo,
    etat_route,
    w_route=0.593,
    w_meteo=0.407,
    alpha=0.30
):
    """
    Fonction 3 : Calcul du coefficient de difficulté Coeff_1
    (pénibilité environnementale).

    Méthode :
    1. Normalisation des notes sur une échelle de 0 à 1 :
       d_route = (5 - etat_route) / 4
       d_meteo = (5 - meteo) / 4

    2. Pondération AHP (Option A - Hors distance) :
       - État de la route : 59.3 %
       - Météo : 40.7 %

    3. Calcul du coefficient final :
       Coeff_1 = 1.0 + (alpha * d_global)

    Plage de variation :
       - 1.000 : conditions idéales (notes de 5/5)
       - 1.300 : conditions dégradées (notes de 1/5),
                 soit une majoration maximale de 30 %.

    Paramètres :
        meteo (int ou float) : Note météo comprise entre 1 et 5.
        etat_route (int ou float) : Note de l'état de la route
                                    comprise entre 1 et 5.
        w_route (float) : Poids AHP de l'état de la route.
        w_meteo (float) : Poids AHP de la météo.
        alpha (float) : Majoration maximale du coefficient.

    Retour :
        float : Coefficient de difficulté arrondi à 3 décimales.
    """

    # 1. Normalisation des notes (échelle de 0 à 1)
    d_route = (5.0 - float(etat_route)) / 4.0
    d_meteo = (5.0 - float(meteo)) / 4.0

    # 2. Calcul du score global de pénibilité (pondération AHP)
    d_global = (
        w_route * d_route
        + w_meteo * d_meteo
    )

    # 3. Calcul du coefficient final
    coeff_1 = 1.0 + (alpha * d_global)

    return round(coeff_1, 3)

# ==============================================================================
# FONCTION 4 : MOTEUR DE CALCUL DU TARIF FINAL
# ==============================================================================

def Obtenir_Tarif(
    wilaya_input,
    vehicule_input,
    df,
    models_dict,
    ratios_vehicules
):
    """
    Calcule le tarif final estimé à partir :
    - du modèle de régression de la zone ;
    - du ratio multiplicateur du véhicule ;
    - du coefficient de difficulté environnementale.

    Paramètres :
        wilaya_input : nom de la wilaya de destination.
        vehicule_input : type de véhicule.
        df : DataFrame nettoyé issu de HALIMA.csv.
        models_dict : modèles LinearRegression par zone.
        ratios_vehicules : ratios multiplicateurs des véhicules.

    Retour :
        Tarif final estimé en DA, ou None si une erreur survient.
    """

    # ------------------------------------------------------------------
    # 1. Recherche de la wilaya
    # ------------------------------------------------------------------

    wilaya_clean = wilaya_input.strip().casefold()

    row = df[
        df["Wilaya"].astype(str).str.strip().str.casefold()
        == wilaya_clean
    ]

    if row.empty:
        print(
            f"\n❌ Erreur : Wilaya '{wilaya_input}' "
            "introuvable dans le fichier HALIMA.csv."
        )

        wilayas_disponibles = df["Wilaya"].dropna().unique()[:10]

        print(
            "Exemples de wilayas disponibles : "
            + ", ".join(wilayas_disponibles)
        )

        return None

    row = row.iloc[0]

    zone = row["Zone"]
    km = float(row["Km"])
    meteo = float(row["Meteo"])
    etat_route = float(row["Etat_Route"])

    # ------------------------------------------------------------------
    # 2. Standardisation du type de véhicule
    # ------------------------------------------------------------------

    veh_mapping = {
        "fourgonnette": "fourgonnette",

        "fourgon 1t5": "Fourgon_1T5",
        "fourgon_1t5": "Fourgon_1T5",
        "1t5": "Fourgon_1T5",
        "1.5t": "Fourgon_1T5",

        "fourgon 2t5": "Fourgon_2T5",
        "fourgon_2t5": "Fourgon_2T5",
        "2t5": "Fourgon_2T5",
        "2.5t": "Fourgon_2T5",

        "camion 3t5": "Camion_3T5",
        "camion_3t5": "Camion_3T5",
        "3t5": "Camion_3T5",
        "3.5t": "Camion_3T5",

        "camion 5t 10t": "Camion_5T_10T",
        "camion_5t_10t": "Camion_5T_10T",
        "5t": "Camion_5T_10T",
        "10t": "Camion_5T_10T",

        "camion 20t": "Camion_20T",
        "camion_20t": "Camion_20T",
        "20t": "Camion_20T"
    }

    vehicule_clean = vehicule_input.strip().casefold()

    key_v = veh_mapping.get(
        vehicule_clean,
        vehicule_input.strip()
    )

    if key_v not in ratios_vehicules:
        print(
            f"\n❌ Erreur : Véhicule '{vehicule_input}' invalide."
        )

        print(
            "Véhicules reconnus : fourgonnette, Fourgon_1T5, "
            "Fourgon_2T5, Camion_3T5, Camion_5T_10T, Camion_20T."
        )

        return None

    # ------------------------------------------------------------------
    # 3. Vérification du modèle de régression de la zone
    # ------------------------------------------------------------------

    if zone not in models_dict:
        print(
            f"\n❌ Erreur : Aucun modèle de régression disponible "
            f"pour la zone '{zone}'."
        )
        return None

    model = models_dict[zone]

    # Prédiction du tarif de base de la fourgonnette
    tarif_base_fourgonnette = float(
        model.predict(np.array([[km]]))[0]
    )

    # ------------------------------------------------------------------
    # 4. Application du ratio du véhicule
    # ------------------------------------------------------------------

    coeff_v = ratios_vehicules[key_v]

    # ------------------------------------------------------------------
    # 5. Calcul du coefficient de difficulté environnementale
    # ------------------------------------------------------------------

    try:
        coeff_1 = calculer_coeff_difficulte(
            meteo=meteo,
            etat_route=etat_route
        )
    except (ValueError, TypeError) as erreur:
        print(
            f"\n❌ Erreur dans les conditions du trajet : {erreur}"
        )
        return None

    # ------------------------------------------------------------------
    # 6. Calcul du tarif final
    # ------------------------------------------------------------------

    tarif_final = (
        tarif_base_fourgonnette
        * coeff_v
        * coeff_1
    )

    # ------------------------------------------------------------------
    # 7. Affichage détaillé du résultat
    # ------------------------------------------------------------------

    a = float(model.intercept_)
    b = float(model.coef_[0])

    print("\n" + "=" * 65)
    print(
        f" DÉTAIL DU TARIF : {str(row['Wilaya']).upper()} "
        f"({key_v})"
    )
    print("=" * 65)

    print(f" • Zone géographique       : {zone}")
    print(f" • Distance kilométrique   : {km:.1f} km")

    print(
        f" • Conditions du trajet    : "
        f"Météo {meteo:.0f}/5 | Route {etat_route:.0f}/5"
    )

    print(
        f" • Tarif de base           : "
        f"{tarif_base_fourgonnette:,.2f} DA"
    )

    print(
        f"   Équation de régression  : "
        f"{a:.2f} + ({b:.2f} × {km:.1f})"
    )

    print(f" • Coefficient véhicule    : x{coeff_v:.2f}")
    print(f" • Coefficient difficulté  : x{coeff_1:.3f}")

    print("-" * 65)

    print(
        f" 💰 TARIF FINAL ESTIMÉ     : "
        f"{tarif_final:,.2f} DA"
    )

    print("=" * 65 + "\n")

    return tarif_final,tarif_base_fourgonnette,coeff_v,coeff_1


if __name__ == "__main__":
    # Chargement des données et des modèles
    df_reg, models, ratios, df_clean = regresser_tarif_par_zone()

    # Saisie des informations
    #wilaya = input("Entrez le nom de la wilaya : ")
    """vehicule = input(
        "Entrez le véhicule (Fourgonnette, Fourgon_1T5, "
        "Fourgon_2T5, Camion_3T5, Camion_5T_10T, Camion_20T) : "
    )"""
    #
    wilaya = "Jijel"
    #wilaya = "Mouzambik"
    vehicule = "Fourgonnette"
    # Calcul et affichage du tarif total
    tarif_total = Obtenir_Tarif(
        wilaya_input=wilaya,
        vehicule_input=vehicule,
        df=df_clean,
        models_dict=models,
        ratios_vehicules=ratios
    )

    if tarif_total is not None:
        print("\n" + "=" * 40)
        print(f"Wilaya : {wilaya}")
        print(f"Véhicule : {vehicule}")
        print(f"Tarif total  : {tarif_total}")
        print("=" * 40)

    else:
        print("\n" + "=" * 40)
        print(f"Not resultat of this wilaya : {wilaya}")
# In[ ]:




