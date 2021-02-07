from flask import Blueprint, render_template,session,request
from flask import current_app, flash, url_for, redirect
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import os, joblib
import pandas as pd
import matplotlib as mpl 
from my_util.weather import get_weather

clf_bp = Blueprint('clf_bp', __name__)
menu = {'ho':0, 'da':0, 'ml':1, 'sc':0, 'co':0, 'ca':0, 'cr':0, 'wc':0, 'clf':1, 'a_clf':0, 'rg':0,'cl':0}


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

@clf_bp.route('/titanic', methods=['GET', 'POST'])
def titanic():
    if request.method == 'GET':
        return render_template('classifier/titanic.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('static/data/titanic_test.csv')
        scaler = joblib.load('static/model/titanic_scaler.pkl')
        test_data = df.iloc[index, :-1].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, 0]
        lrc = joblib.load('static/model/titanic_lr.pkl')
        svc = joblib.load('static/model/titanic_sv.pkl')
        rfc = joblib.load('static/model/titanic_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)
        result = {'index':index, 'label':label,
                  'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_rf':pred_rf[0]}

        tmp = df.iloc[index, 1:].values
        value_list = []
        int_index_list = [0, 1, 3, 4, 6, 7]
        for i in range(8):
            if i in int_index_list:
                value_list.append(int(tmp[i]))
            else:
                value_list.append(tmp[i])
        org = dict(zip(df.columns[1:], value_list))
        return render_template('classifier/titanic_res.html', menu=menu, 
                                res=result, org=org, weather=get_weather())

@clf_bp.route('/pima', methods=['GET', 'POST'])
def pima():
    if request.method == 'GET':
        return render_template('classifier/pima.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('static/data/pima_test.csv')
        scaler = joblib.load('static/model/pima_scaler.pkl')
        test_data = df.iloc[index, :-1].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/pima_lr.pkl')
        svc = joblib.load('static/model/pima_sv.pkl')
        rfc = joblib.load('static/model/pima_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)
        result = {'index':index, 'label':label,
                  'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_rf':pred_rf[0]}
        org = dict(zip(df.columns[:-1], df.iloc[index, :-1]))
        return render_template('classifier/pima_res.html', menu=menu, 
                                res=result, org=org, weather=get_weather())

@clf_bp.route('/breast', methods=['GET', 'POST'])
def breast():
    if request.method == 'GET':
        return render_template('classifier/breast.html', menu=menu, weather=get_weather_main())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('./static/data/breast_test.csv')
        scaler = joblib.load('static/model/breast_scale.pkl')
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

@clf_bp.route('/iris', methods=['GET', 'POST'])
def iris():
    if request.method == 'GET':
        return render_template('classifier/iris.html', menu=menu, weather=get_weather_main())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('static/data/iris_test.csv')
        scaler = joblib.load('static/model/iris_scaler.pkl')
        test_data = df.iloc[index, :-1].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/iris_lr.pkl')
        svc = joblib.load('static/model/iris_sv.pkl')
        rfc = joblib.load('static/model/iris_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)

        species = ['Setosa', 'Versicolor', 'Virginica']
        result = {'index':index, 'label':f'{label} ({species[label]})',
                  'pred_lr':f'{pred_lr[0]} ({species[pred_lr[0]]})', 
                  'pred_sv':f'{pred_sv[0]} ({species[pred_sv[0]]})', 
                  'pred_rf':f'{pred_rf[0]} ({species[pred_rf[0]]})'}
        org = dict(zip(df.columns[:-1], df.iloc[index, :-1]))
        return render_template('classifier/iris_res.html', menu=menu, weather=get_weather_main(),res=result,org=org)

@clf_bp.route('/wine', methods=['GET', 'POST'])
def wine():
    if request.method == 'GET':
        return render_template('classifier/wine.html', menu=menu, weather=get_weather_main())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('static/data/wine_test.csv')
        scaler = joblib.load('static/model/wine_scaler.pkl')
        test_data = df.iloc[index, :-1].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/wine_lr.pkl')
        svc = joblib.load('static/model/wine_sv.pkl')
        rfc = joblib.load('static/model/wine_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)
        result = {'index':index, 'label':label,
                  'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_rf':pred_rf[0]}
        org = dict(zip(df.columns[:-1], df.iloc[index, :-1]))
        return render_template('classifier/wine_res.html', menu=menu, weather=get_weather_main(),res=result,org=org)
