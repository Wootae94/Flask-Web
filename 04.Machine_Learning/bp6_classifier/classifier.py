from flask import Blueprint, render_template,session,request
from flask import current_app, flash, url_for, redirect
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
import os, joblib
import pandas as pd
import matplotlib as mpl 
from my_util.weather import get_weather

clf_bp = Blueprint('clf_bp', __name__)


def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        current_app.logger.debug("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)
    return weather

@clf_bp.route('/breast', methods=['GET', 'POST'])
def breast():
    menu = {'ho':0, 'da':0, 'ml':1, 'sc':0, 'co':0, 'ca':0, 'cr':0, 'wc':0, 'clf':1, 'a_clf':0, 'rg':0,'cl':0}
    if request.method == 'GET':
        return render_template('classifier/breast.html', menu=menu, weather=get_weather_main())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('./static/data/breast_test.csv')
        scaler = StandardScaler()
        scaled_test = scaler.fit_transform(df.iloc[:, :-1])
        test_data = scaled_test[index, :].reshape(1,-1)
        label = df.iloc[index, -1]
        dtclf = joblib.load('static/model/best_breast_dtclf.pkl')
        knn = joblib.load('static/model/best_breast_knn.pkl')
        lr = joblib.load('static/model/best_breast_lr.pkl')
        rfclf = joblib.load('static/model/best_breast_rfclf.pkl')
        svc = joblib.load('static/model/best_breast_svc.pkl')
        pred_dtclf = dtclf.predict(test_data)
        pred_knn = knn.predict(test_data)
        pred_lr = lr.predict(test_data)
        pred_rfclf = rfclf.predict(test_data)
        pred_svc = svc.predict(test_data)
        result = {'index':index, 'label':label,
                  'pred_lr':pred_lr[0], 'pred_dtclf':pred_dtclf[0], 'pred_knn':pred_knn[0],'pred_rfclf':pred_rfclf[0],'pred_svc':pred_svc[0]}
        org = dict(zip(df.columns[:-1], df.iloc[index, :-1]))
        return render_template('classifier/breast_res.html', menu=menu, weather=get_weather_main(),res=result,org=org)
