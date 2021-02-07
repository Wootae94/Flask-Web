from flask import Blueprint, render_template, request, session, g
from flask import current_app
from werkzeug.utils import secure_filename
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import os
import pandas as pd
import matplotlib.pyplot as plt 
from my_util.weather import get_weather
from my_util.clustering import clustering
cluster_bp = Blueprint('cluster_bp', __name__)

def get_weather_main():
    ''' weather = None
    try:
        weather = session['weather']
    except:
        current_app.logger.info("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=60) '''
    weather = get_weather()
    return weather

@cluster_bp.route('/cluster', methods=['GET', 'POST'])
def cluster():
    menu = {'ho':0, 'da':0, 'ml':1, 'sc':0, 'co':0, 'ca':0, 'cr':0, 'wc':0, 'clf':0, 'a_clf':0, 'rg':0,'cl':1}
    if request.method == 'GET':
        return render_template('cluster/cluster.html', menu=menu, weather=get_weather_main())
    else:
        k_number = int(request.form['k_number'])
        f_csv = request.files['csv']
        file_csv = os.path.join(current_app.root_path, 'static/upload/') + f_csv.filename
        f_csv.save(file_csv)
        current_app.logger.debug(f"{k_number}, {f_csv}, {file_csv}")

        df_csv = pd.read_csv(file_csv)
        mtime = clustering(df_csv, k_number)
        return render_template('cluster/cluster_res.html', menu=menu, weather=get_weather_main(),
                                k_number=k_number, mtime=mtime)