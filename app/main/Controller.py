from flask import request,Blueprint,render_template,jsonify
from app.code.tarification_hybride import *
#
blueprint_main = Blueprint(
    'main',
    __name__,
    #template_folder='../templates',
    url_prefix='/'
)
#
@blueprint_main.route('/')
def index():
   return render_template('public.html')
#
@blueprint_main.route('/recalculate')
def recalculate():
    #
    wilaya = request.args.get('destination')
    distance = request.args.get('distance')
    vehicule = request.args.get('vehicule')
    manutention = request.args.get('manutention')
    poid = request.args.get('poid')
    dangereux= request.args.get('dangereux')
    #
    print("wilaya ==>",wilaya)
    print("distance==>",distance)
    print("vehicule==>",vehicule)
    #
    df_reg, models, ratios, df_clean, src_file = regresser_tarif_par_zone("./app/code/halima22.csv")
    # Calcul et affichage du tarif total
    try:
        tarif_total,tarif_base,coeff_v,coeff_i,km,temp=  Obtenir_Tarif(
            wilaya,
            vehicule,
            df_clean,
            models,
            ratios,
            nom_fichier_source=src_file)
        #
        print("tarif_total==>",tarif_base)
        #
        if tarif_total :
            data = {
                'code':200,
                'wilaya':wilaya,
                'distance':distance,
                'vehicule':vehicule,
                'tarif_total':tarif_total,
                'tarif_base':tarif_base,
                'coeff_v':coeff_v,
                'coeff_i':coeff_i,
                'distance':km,
                'dure':temp
            }
        else:
            data = {
                'code':400,
                'wilaya':wilaya,
            }
            #
        return jsonify(data)
    except Exception as e:
        data = {
            'code': 500,
            'wilaya': wilaya,
            'error': str(e)
        }
        #
        return jsonify(data)