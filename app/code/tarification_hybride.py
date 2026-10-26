#!/usr/bin/env python
# coding: utf-8

"""
MODULE DE TARIFICATION HYBRIDE - LOGISTIQUE ALGÉRIE
---------------------------------------------------
Fichier source principal : halima2.csv (ou HALIMA.csv)

Règles Métier :
1. PRIX HISTORIQUE FIXE : Si la wilaya et le type de véhicule existent avec un prix
   dans halima2.csv, le script renvoie directement la valeur réelle enregistrée.
2. ESTIMATION SUR NOUVELLES DESTINATIONS : Si le tarif ou la ville est absent, 
   le script applique la régression linéaire par zone (Tarif_Base = a + b * Km) 
   multipliée par le coefficient du véhicule (x1.00 à x2.32).
"""

import csv
import io
import re
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# ==============================================================================
# 1. OUTILS DE LECTURE ET NORMALISATION
# ==============================================================================
def _lire_lignes(filepath):
    """Lit un .xlsx ou un .csv (séparateur ';', ',' ou tabulation, avec ou sans BOM)."""
    if str(filepath).lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        ws = openpyxl.load_workbook(filepath, data_only=True).active
        return [["" if c is None else c for c in row] for row in ws.iter_rows(values_only=True)]

    with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
        texte = f.read()
    delim = ";" if ";" in texte else ("\t" if "\t" in texte else ",")
    return list(csv.reader(io.StringIO(texte), delimiter=delim))


def _detecter_convention(lignes):
    """Détecte la convention numérique (US vs FR)."""
    for ligne in lignes:
        for c in ligne:
            s = str(c)
            if "," in s and "." in s and re.fullmatch(r"[\s\d.,\-]+", s):
                return "US" if s.rfind(".") > s.rfind(",") else "FR"
    return None


def _en_nombre(x, convention=None):
    """Convertit une chaîne nettoyée en nombre float."""
    if isinstance(x, (int, float, np.integer, np.floating)):
        return float(x)
    s = str(x).strip().replace("\xa0", "").replace("\u202f", "").replace(" ", "")
    if s in ("", "-", "nan", "None"):
        return np.nan
    if convention == "US":
        s = s.replace(",", "")
    elif convention == "FR":
        s = s.replace(".", "").replace(",", ".")
    else:
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
    """Normalise le nom de la zone géographique."""
    m = re.match(r"^\s*(CENTRE|EST|OUEST|MOYEN_SUD|GRAND_SUD|SUD)\s*-?\s*(\d*)\s*$", str(texte), re.IGNORECASE)
    if m:
        z = m.group(1).upper()
        if z == "SUD":
            z = "MOYEN_SUD"
        return z
    return None


# ==============================================================================
# 2. RÉGRESSION DES TARIFS PAR ZONE ET CALCUL DES RATIOS VÉHICULES
# ==============================================================================
def regresser_tarif_par_zone(filepath_halima="halima2.csv"):
    """
    Lit le fichier halima2.csv (ou alternative), construit les modèles de régression
    par zone géographique et calcule les ratios moyens par type de véhicule.
    """
    chemins_possibles = [
        filepath_halima,
        os.path.join("/workspace/knowledge", filepath_halima),
        "halima2.csv",
        "/workspace/knowledge/halima2.csv",
        "HALIMA.csv",
        "/workspace/knowledge/HALIMA.csv"
    ]
    
    fichier_trouve = None
    for p in chemins_possibles:
        if os.path.exists(p):
            fichier_trouve = p
            break
            
    if not fichier_trouve:
        raise FileNotFoundError(f"Impossible de trouver le fichier source {filepath_halima}.")

    lignes = _lire_lignes(fichier_trouve)
    convention = _detecter_convention(lignes)
    
    rows, zone = [], None
    for ligne in lignes:
        if not ligne or not any(str(c).strip() for c in ligne):
            continue
        first = str(ligne[0]).strip()
        z = _zone(first)
        if z:
            zone = z
            continue
        if first.lower() in ("wilayas", "wilaya"):
            continue
        if zone and first and len(ligne) >= 7:
            cellules = list(ligne[1:])
            cellules += [""] * (13 - len(cellules))
            rows.append([zone, first] + cellules)

    cols = ['Zone', 'Wilaya', 'fourgonnette', 'Fourgon_1T5', 'Fourgon_2T5',
            'Camion_3T5', 'Camion_5T_7T', 'Camion_10T', 'Camion_20T', 'Camion_40T', 
            'Km', 'Temps', 'Meteo', 'Etat_Route']
    
    df = pd.DataFrame([r[:14] for r in rows], columns=cols)

    num_cols = ['fourgonnette', 'Fourgon_1T5', 'Fourgon_2T5', 'Camion_3T5',
                'Camion_5T_7T', 'Camion_10T', 'Camion_20T', 'Camion_40T', 'Km', 'Meteo', 'Etat_Route']
    for col in num_cols:
        df[col] = df[col].map(lambda v: _en_nombre(v, convention))

    # Re-classification en GRAND_SUD pour les trajets de plus de 1000 km
    for idx, row_item in df.iterrows():
        if pd.notna(row_item['Km']) and float(row_item['Km']) > 1000:
            df.at[idx, 'Zone'] = 'GRAND_SUD'

    zones = list(dict.fromkeys(df['Zone']))
    veh_cols = ['Fourgon_1T5', 'Fourgon_2T5', 'Camion_3T5', 'Camion_5T_7T', 'Camion_10T', 'Camion_20T', 'Camion_40T']

    # 1. Modèles de régression par zone sur la fourgonnette (Base = 1.00)
    obs = df[df['Km'].notna() & df['fourgonnette'].notna()]
    models_dict, reg_results = {}, []
    for z in zones:
        grp = obs[obs['Zone'] == z]
        if len(grp) < 2:
            continue
        X, y = grp[['Km']].values, grp['fourgonnette'].values
        model = LinearRegression().fit(X, y)
        models_dict[z] = model
        a, b = float(model.intercept_), float(model.coef_[0])
        reg_results.append({
            'Zone': z,
            'Nombre_Trajets': len(grp),
            'Frais_Fixe_a_DA': round(a, 2),
            'Tarif_Km_b_DA': round(b, 2),
            'R2': round(model.score(X, y), 4),
            'Equation': f"T_base = {a:.2f} + {b:.2f} * Km",
        })
    df_regres = pd.DataFrame(reg_results)

    # 2. Calcul des ratios réels par rapport à la fourgonnette
    ratios = {'fourgonnette': 1.0}
    for col in veh_cols:
        sous = obs.dropna(subset=[col])
        sous = sous[sous['fourgonnette'] > 0]
        if not sous.empty:
            ratios[col] = float((sous[col] / sous['fourgonnette']).mean())
        else:
            ratios[col] = 1.0

    return df_regres, models_dict, ratios, df, fichier_trouve


# ==============================================================================
# 3. CALCUL DU COEFFICIENT DE PÉNIBILITÉ (OPTIONNEL)
# ==============================================================================
def calculer_coeff_difficulte(meteo, etat_route, w_route=0.593, w_meteo=0.407, alpha=0.30):
    d_route = (5.0 - float(etat_route)) / 4.0
    d_meteo = (5.0 - float(meteo)) / 4.0
    d_global = (w_route * d_route) + (w_meteo * d_meteo)
    coeff_1 = 1.0 + (alpha * d_global)
    return round(coeff_1, 3)


# ==============================================================================
# 4. MOTEUR DE CALCUL HYBRIDE DU TARIF (LE CŒUR DU SYSTÈME)
# ==============================================================================
def Obtenir_Tarif(
    wilaya_input,
    vehicule_input,
    df,
    models_dict,
    ratios_vehicules,
    km_input=None,
    zone_input=None,
    meteo_input=5.0,
    etat_route_input=5.0,
    appliquer_penibilite_exceptionnelle=False,
    nom_fichier_source="halima2.csv"
):
    """
    Logique Hybride :
    1. Si la Wilaya ET le Véhicule existent dans halima2.csv avec un prix :
       -> Renvoyer DIRECTEMENT le tarif fixe historique.
    2. Si la Wilaya est NOUVELLE ou le prix est absent :
       -> Calculer l'estimation : Tarif = Tarif_Base_Zone(Km) * Ratio_Vehicule
    """

    veh_mapping = {
        "fourgonnette": "fourgonnette",
        "fourgon 1t5": "Fourgon_1T5", "fourgon_1t5": "Fourgon_1T5", "1t5": "Fourgon_1T5",
        "fourgon 2t5": "Fourgon_2T5", "fourgon_2t5": "Fourgon_2T5", "2t5": "Fourgon_2T5",
        "camion 3t5": "Camion_3T5", "camion_3t5": "Camion_3T5", "3t5": "Camion_3T5",
        "camion 5t 7t": "Camion_5T_7T", "camion 5t": "Camion_5T_7T", "camion_5t_7t": "Camion_5T_7T", "5t": "Camion_5T_7T",
        "camion 10t": "Camion_10T", "camion_10t": "Camion_10T", "10t": "Camion_10T",
        "camion 20t": "Camion_20T", "camion_20t": "Camion_20T", "20t": "Camion_20T",
        "camion 40t": "Camion_40T", "camion_40t": "Camion_40T", "40t": "Camion_40T"
    }

    veh_clean = vehicule_input.strip().casefold()
    col_veh = veh_mapping.get(veh_clean, vehicule_input.strip())

    wilaya_clean = wilaya_input.strip().casefold()
    row = df[df["Wilaya"].astype(str).str.strip().str.casefold() == wilaya_clean]

    # CAS 1 : Wilaya et Prix du véhicule EXISTENT dans l'historique
    if not row.empty:
        row_data = row.iloc[0]
        val_historique = row_data.get(col_veh)

        if pd.notna(val_historique) and float(val_historique) > 0:
            tarif_exact = float(val_historique)
            print("\n" + "=" * 65)
            print(f" 📌 TARIF HISTORIQUE FIXE : {row_data['Wilaya'].upper()} ({col_veh})")
            print("=" * 65)
            print(f" • Source                   : Barème Officiel ({os.path.basename(nom_fichier_source)})")
            print(f" • Zone                     : {row_data['Zone']}")
            print(f" • Distance                 : {row_data['Km']} km")
            print(f" • Temps estimé             : {row_data['Temps']}")
            print("-" * 65)
            print(f" 💰 TARIF FINAL HISTORIQUE  : {tarif_exact:,.2f} DA")
            print("=" * 65 + "\n")
            return tarif_exact,tarif_exact,0,0,row_data['Km'],row_data['Temps']

    # CAS 2 : Wilaya NOUVELLE ou véhicule non tarifé (ESTIMATION PAR FORMULE)
    print(f"\nℹ️  Wilaya/Véhicule absent de la grille fixe. Calcul de l'estimation pour '{wilaya_input}' ({col_veh})...")

    if not row.empty:
        row_data = row.iloc[0]
        zone = row_data["Zone"]
        km = float(row_data["Km"]) if pd.notna(row_data["Km"]) else (float(km_input) if km_input else 0.0)
        meteo = float(row_data.get("Meteo", 5.0)) if pd.notna(row_data.get("Meteo")) else 5.0
        etat_route = float(row_data.get("Etat_Route", 5.0)) if pd.notna(row_data.get("Etat_Route")) else 5.0
    else:
        if km_input is None:
            print(f"❌ Erreur : Pour une nouvelle wilaya ('{wilaya_input}'), veuillez fournir au moins la distance (Km).")
            return None
        km = float(km_input)
        zone = zone_input.upper() if zone_input else ("GRAND_SUD" if km > 1000 else ("MOYEN_SUD" if km > 150 else "CENTRE"))
        meteo = float(meteo_input)
        etat_route = float(etat_route_input)

    if km > 1000:
        zone = "GRAND_SUD"

    model = models_dict.get(zone)
    if not model and zone == "GRAND_SUD":
        a, b = 11972.02, 69.98
        tarif_base_fourgonnette = a + (b * km)
    elif model:
        a = float(model.intercept_)
        b = float(model.coef_[0])
        pred = model.predict(np.array([[km]]))
        tarif_base_fourgonnette = float(pred[0][0]) if pred.ndim > 1 else float(pred[0])
    else:
        a, b = 12000.0, 50.0
        tarif_base_fourgonnette = a + (b * km)

    coeff_v = ratios_vehicules.get(col_veh, 1.0)

    coeff_penibilite = 1.0
    if appliquer_penibilite_exceptionnelle:
        coeff_penibilite = calculer_coeff_difficulte(meteo, etat_route)

    tarif_estime = tarif_base_fourgonnette * coeff_v * coeff_penibilite

    print("\n" + "=" * 65)
    print(f" 🧮 ESTIMATION DU TARIF : {wilaya_input.upper()} ({col_veh})")
    print("=" * 65)
    print(f" • Source données de base   : {os.path.basename(nom_fichier_source)}")
    print(f" • Zone appliquée           : {zone}")
    print(f" • Distance kilométrique    : {km:.1f} km")
    print(f" • Temp    : {row_data["Temps"]} km")
    print(f" • Tarif Base Fourgonnette  : {tarif_base_fourgonnette:,.2f} DA  [ {a:.2f} + ({b:.2f} × {km:.1f}) ]")
    print(f" • Coefficient Véhicule     : x{coeff_v:.2f}")
    if appliquer_penibilite_exceptionnelle:
        print(f" • Major. Pénibilité Extrême: x{coeff_penibilite:.3f}")
    print("-" * 65)
    print(f" 💰 TARIF FINAL ESTIMÉ      : {tarif_estime:,.2f} DA")
    print("=" * 65 + "\n")

    return tarif_estime,tarif_base_fourgonnette,coeff_v,coeff_penibilite,km,row_data["Temps"]


# ==============================================================================
# TEST D'EXÉCUTION DU MODULE
# ==============================================================================
if __name__ == "__main__":
    df_reg, models, ratios, df_clean, src_file = regresser_tarif_par_zone("halima22.csv")

    print(f"--> Modèles et Ratios chargés avec succès depuis : {src_file}\n")

    # Exemple 1 : Ville existante dans halima2.csv
    Obtenir_Tarif("Oran", "Camion 20T", df_clean, models, ratios, nom_fichier_source=src_file)

    # Exemple 2 : Ville distante dans halima2.csv sans prix fixe rempli (Bordj Badji Mokhtar)
    a= Obtenir_Tarif("Bordj Badji Mokhtar", "Camion 20T", df_clean, models, ratios, nom_fichier_source=src_file)
    #
    print(a)
