from flask import Blueprint, render_template, request, session
from flask import current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
from datetime import timedelta, datetime
import os, folium, json
import pandas as pd
import matplotlib as mpl 
import matplotlib.pyplot as plt

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from my_util.weather import get_weather
from db.db_module import get_covid_daily,get_agender_daily,get_region_daily,get_region_list,get_covid_region,get_region_offset,get_region_pred
from my_util.covid_util import new_covid_daily,new_covid_agender,new_covid_region,draw_seoul_line,draw_seoul_bar

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
    
@covid_bp.route('/region',methods = ['GET'])
def covid_region():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    today = datetime.now().strftime('%Y-%m-%d')
    date = request.args.get("date",today+' '+today)
    current_app.logger.info(f'{date}  data')
    try:
        start = date.split(' ')[0]
        end = date.split(' ')[1]
        rows = get_region_pred(start,end)
        current_app.logger.info(f'{start}-{end}  data')
    except:
        current_app.logger.error('Data error')
        flash(f'날짜를 다시 선택해주십시오','danger')
        return redirect(url_for('covid_bp.covid_region'))
    return render_template('covid/region.html', menu=menu, weather=get_weather_main(),rows=rows,date=start)  

  

@covid_bp.route('/agender/chart/radar',methods = ['GET'])
def age_radar():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    today = datetime.now().strftime('%Y-%m-%d')
    date = request.args.get("date",today)
    current_app.logger.info(f'{date}  data ')
    rows = get_agender_daily(date)
    data1_list,data2_list,data3_list = [],[],[]
    for row in rows[:-2]:
        data1_list.append(row[2])
        data2_list.append(row[4])
        data3_list.append(row[5])
    data_dict = {"data1":data1_list,"data2":data2_list,"data3":data3_list}
    return render_template('covid/agender_radar.html', menu=menu, weather=get_weather_main(),date=date,data_dict=data_dict)  

@covid_bp.route('/daily/chart/line',methods = ['GET'])
def daily_line():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    region_list = get_region_list()
    region = request.args.get("region","합계")
    offset = get_region_offset(region) - 10
    current_app.logger.info(f'{region}  data ')
    rows = get_covid_region(region,offset)
    date_list,defCnt_list,isolClearCnt_list = [],[],[]
    for row in rows:
        date_list.append(row[0])
        defCnt_list.append(row[2])
        isolClearCnt_list.append(row[5])
    data_dict = {"date":date_list,"defCnt":defCnt_list,"isolClearCnt":isolClearCnt_list}
    return render_template('covid/daily_line.html', menu=menu, weather=get_weather_main(),region_list=region_list,data_dict=data_dict,subject=region)  

@covid_bp.route('/region/chart/doughnut',methods = ['GET'])
def region_doughnut():
    
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    today = datetime.now().strftime('%Y-%m-%d')
    date = request.args.get("date",today)
    rows = get_region_daily(date)
    region_list = ['제주','경남','경북','전남','전북','충남','충북','강원','경기','세종','울산','대전','광주','인천','대구','부산','서울']
    data_list = rows[0][1:-1]
    data_dict = {"region":region_list,"data":data_list}
    current_app.logger.info(f'{data_list}  data ')
    return render_template('covid/region_doughnut.html', menu=menu, weather=get_weather_main(),date=date, data_dict=data_dict)


@covid_bp.route('/update_daily/<path:path>',methods = ['GET'])
def update_covid_daily(path):
    date = ''.join(path.split('-'))
    current_app.logger.info(f'{date}  data ')
    try:
        current_app.logger.info(f'data success')
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

@covid_bp.route('/update_region/<path:path>',methods = ['GET'])
def update_covid_region(path):
    current_app.logger.info(f'{path} 입력  data ')
    try:
        new_covid_region(path)
    except:
        current_app.logger.error('Data error')
        flash('아직 데이터가 없습니다.','danger')
        return redirect(url_for('covid_bp.covid_region')+f'?date={path} {path}')
    
    return redirect(url_for('covid_bp.covid_region')+f'?date={path} {path}')

@covid_bp.route('/seoul_trend',methods = ['GET','POST'])
def seoul_trend():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    if request.method =='GET':
        gu = request.args.get("gu","합계")
        today = datetime.now().strftime('%Y-%m-%d')
        date_list = ['2020-03-02',today]
        col_list = draw_seoul_line([gu],date_list)[0]
        mtime = draw_seoul_line([gu],date_list)[1]
        return render_template('covid/seoul_trend.html', menu=menu, weather=get_weather_main(),col_list=col_list,mtime=mtime)
    else:
        gu_list = request.form.getlist('gu') 
        date_list = request.form.getlist('dateCustomer')
        current_app.logger.info(f'{gu_list}')
        col_list = draw_seoul_line(gu_list,date_list)[0]
        mtime = draw_seoul_line(gu_list,date_list)[1]
        
        return render_template('covid/seoul_trend.html', menu=menu, weather=get_weather_main(),mtime=mtime,col_list=col_list)

@covid_bp.route('/seoul_compare',methods = ['GET','POST'])
def seoul_compare():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    if request.method == 'GET':
        subject = request.args.get('subject','인구수당누적확진자수')
        mtime = draw_seoul_bar(subject)
        return render_template('covid/seoul_compare.html', menu=menu, weather=get_weather_main(),mtime=mtime)
    else: 
        subject = request.form['subject']
        current_app.logger.info(subject)
        mtime = draw_seoul_bar(subject)
        return render_template('covid/seoul_compare.html', menu=menu, weather=get_weather_main(),mtime=mtime)

@covid_bp.route('/seoul_covidmap',methods = ['GET'])
def seoul_covidmap():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':1, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    geo_path = './static/data/skorea_municipalities_geo_simple.json'
    geo_str = json.load(open(geo_path, encoding='utf8'))
    corona_gu = pd.read_csv('./static/data/구별 코로나.csv',index_col='지역')
    subject = request.args.get('subject','인구수당누적확진자수')
    subtitle = subject
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11,
            tiles='Stamen Toner')
    map.choropleth(geo_data = geo_str,
            data = corona_gu[subject],
            columns = [corona_gu.index, corona_gu[subject]],
            fill_color = 'YlGnBu',
            key_on = 'feature.id')
    map.save('templates/map.html')
    return render_template('covid/seoul_covidmap.html', menu=menu, weather=get_weather_main(),subtitle=subtitle)  