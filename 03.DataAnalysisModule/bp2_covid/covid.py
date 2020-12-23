from flask import Blueprint, render_template, request, session
from flask import current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
from datetime import timedelta, datetime
import os, folium, json
import pandas as pd
from my_util.weather import get_weather
from db.db_module import get_covid_daily,get_agender_daily,get_region_list,get_covid_region
from my_util.covid_util import new_covid_daily,new_covid_agender

covid_bp = Blueprint('covid_bp', __name__)

def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        current_app.logger.info("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=60)
    return weather

@covid_bp.route('/daily',methods = ['GET'])
def covid_daily():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    today = datetime.now().strftime('%Y-%m-%d')
    date = request.args.get("date",today)
    rows = get_covid_daily(date)
    return render_template('covid/daily.html', menu=menu, weather=get_weather_main(),date=date, rows=rows)  
    
@covid_bp.route('/agender',methods = ['GET'])
def covid_agender():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    today = datetime.now().strftime('%Y-%m-%d')
    date = request.args.get("date",today)
    rows = get_agender_daily(date)
    return render_template('covid/agender.html', menu=menu, weather=get_weather_main(),date=date, rows=rows)  

@covid_bp.route('/agender/chart/radar/<path:path>',methods = ['GET'])
def age_radar(path):
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    date = path
    current_app.logger.info(f'{date}  data ')
    rows = get_agender_daily(date)
    data1_list,data2_list,data3_list = [],[],[]
    for row in rows[:-2]:
        data1_list.append(row[2])
        data2_list.append(row[4])
        data3_list.append(row[5])
    data_dict = {"data1":data1_list,"data2":data2_list,"data3":data3_list}
    return render_template('covid/agender_radar.html', menu=menu, weather=get_weather_main(),date=path,data_dict=data_dict)  

@covid_bp.route('/daily/chart/line',methods = ['GET'])
def daily_line():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    region_list = get_region_list()
    region = request.args.get("region","합계")
    current_app.logger.info(f'{region}  data ')
    rows = get_covid_region(region)
    date_list,defCnt_list,isolClearCnt_list = [],[],[]
    for row in rows:
        date_list.append(row[0])
        defCnt_list.append(row[2])
        isolClearCnt_list.append(row[5])
    data_dict = {"date":date_list,"defCnt":defCnt_list,"isolClearCnt":isolClearCnt_list}
    return render_template('covid/daily_line.html', menu=menu, weather=get_weather_main(),region_list=region_list,data_dict=data_dict)  

@covid_bp.route('/update_daily/<path:path>',methods = ['GET'])
def update_covid_daily(path):
    date = ''.join(path.split('-'))
    current_app.logger.info(f'{date}  data ')
    try:
        new_covid_daily(date)
    except:
        current_app.logger.error('Data error')
        flash('아직 데이터가 없습니다.','danger')
        return redirect(url_for('covid_bp.covid_daily')+f'?date={path}')
    return redirect(url_for('covid_bp.covid_daily')+f'?date={path}') 

@covid_bp.route('/update_agender/<path:path>',methods = ['GET'])
def update_covid_agender(path):
    date = ''.join(path.split('-'))
    current_app.logger.info(f'{date}  data ')
    try:
        new_covid_agender(date)
    except:
        current_app.logger.error('Data error')
        flash('아직 데이터가 없습니다.','danger')
        return redirect(url_for('covid_bp.covid_agender')+f'?date={path}')
    
    return redirect(url_for('covid_bp.covid_agender')+f'?date={path}') 