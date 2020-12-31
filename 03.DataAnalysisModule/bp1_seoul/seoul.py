
from flask import Blueprint, render_template, session,request
import folium
import pandas as pd
import json
from datetime import datetime, timedelta
from my_util.weather import get_weather
from flask import current_app
import numpy as np
import matplotlib as mpl 
import matplotlib.pyplot as plt
import os
seoul_bp = Blueprint('seoul_bp', __name__)

seoul_park = pd.read_csv('./static/data/Seoul_Park.csv')
park_list = seoul_park['공원명'].tolist()
gu_park = pd.read_csv('./static/data/gu_park.csv')
gu_list = gu_park['지역구'].tolist()
gu_park = pd.read_csv('./static/data/gu_park.csv',index_col='지역구')

seoul_crime = pd.read_csv('./static/data/Seoul_crime.csv',index_col='구별')
seoul_police = pd.read_csv('./static/data/Seoul_police.csv')
seoul_cctv = pd.read_csv('./static/data/CCTV_result.csv',index_col='구별')
geo_path = './static/data/skorea_municipalities_geo_simple.json'
geo_str = json.load(open(geo_path, encoding='utf8'))

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

@seoul_bp.route('/park', methods=['GET', 'POST'])
def park():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':1, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    if request.method == 'GET':
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
        for i in seoul_park.index:
            folium.CircleMarker([seoul_park.lat[i], seoul_park.lng[i]], 
                        radius=int(seoul_park['반지름'][i]*3),
                        tooltip=f"{seoul_park['공원명'][i]}({int(seoul_park['면적'][i])}㎡)",
                        color='#3186cc', fill_color='#3186cc').add_to(map)
        map.save('templates/map.html')
        return render_template('seoul/park.html', menu=menu, weather=get_weather(), park_list=park_list, gu_list=gu_list)
    else:
        gubun = request.form['gubun']
        if gubun == 'name':
            park_name = request.form['park_name']
            df = seoul_park[seoul_park['공원명']==park_name].reset_index(drop=True)
            park_select = df.loc[0,:].tolist()
            map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
            for i in seoul_park.index:
                folium.CircleMarker([seoul_park.lat[i], seoul_park.lng[i]], 
                            radius=int(seoul_park['반지름'][i]*3),
                            tooltip=f"{seoul_park['공원명'][i]}({int(seoul_park['면적'][i])}㎡)",
                            color='#3186cc', fill_color='#3186cc').add_to(map)
            folium.CircleMarker([df.lat[0], df.lng[0]], 
                            radius=int(df['반지름'][0]*3),
                            tooltip=f"{df['공원명'][0]}({int(df['면적'][0])}㎡)",
                            color='crimson', fill_color='crimson').add_to(map)
            map.save('templates/map.html')
            return render_template('seoul/park_res.html', menu=menu, weather=get_weather(), park_select=park_select)
        else:
            seoul_gu = request.form['seoul_gu']
            df = seoul_park[seoul_park['지역구']==seoul_gu].reset_index(drop=True)
            df2 = gu_park[gu_park.index==seoul_gu].reset_index()
            gu_select = df2.loc[0,:].tolist()
            park_mean = gu_park.mean().round(2).tolist()
            map = folium.Map(location=[df.lat.mean(),df.lng.mean()], zoom_start=11)
            for i in df.index:
                folium.CircleMarker([df.lat[i], df.lng[i]], 
                            radius=int(df['반지름'][i]*3),
                            tooltip=f"{df['공원명'][i]}({int(df['면적'][i])}㎡)",
                            color='#3186cc', fill_color='#3186cc').add_to(map)
            map.save('templates/map.html')
            return render_template('seoul/park_res2.html', menu=menu, weather=get_weather_main(),gu_select=gu_select,park_mean=park_mean)                

@seoul_bp.route('/park_gu')
def park_gu():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':1, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    subtitle = '공원 위치와 크기'
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Stamen Toner')
    for i in seoul_park.index:
        folium.CircleMarker([seoul_park.lat[i], seoul_park.lng[i]], 
                            radius=int(seoul_park['반지름'][i]),
                            tooltip=f"{seoul_park['공원명'][i]}({int(seoul_park['면적'][i])}㎡)",
                            color='green', fill_color='green').add_to(map)
    map.save('templates/map.html')
    return render_template('seoul/park_gu.html', menu=menu, weather=get_weather_main(),subtitle=subtitle)                

@seoul_bp.route('/park_gu/<path:path>')
def park_gu2(path):
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':1, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    path_dict = {'area':'공원총면적','area_ratio':'공원 면적비율','per_person':'인구수당면적','number':'공원 갯수'}
    column_index = path_dict[path]
    subtitle = f'자치구별 {column_index}'
    map = folium.Map(location=[37.55277229023488, 126.99057136537], zoom_start=11,
                tiles='Stamen Toner')
    map.choropleth(geo_data = geo_str,
                    data = gu_park[column_index],
                    columns = [gu_park.index,gu_park[column_index]],
                    fill_color = 'PuRd',
                    key_on = 'feature.id')
    map.save('templates/map.html')
    return render_template('seoul/park_gu.html', menu=menu, weather=get_weather_main(),subtitle=subtitle)     

@seoul_bp.route('/crime')
def crime():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':1, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    subtitle = '서울 관내 경찰서 위치'
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11,
                 tiles='Stamen Toner')
    for i in seoul_police.index:
        folium.CircleMarker([seoul_police.lat[i], seoul_police.lng[i]], radius=10,
                        tooltip=seoul_police['관서명'][i],
                        color='#3186cc', fill_color='#3186cc').add_to(map)
    map.save('templates/map.html')
    return render_template('seoul/crime.html', menu=menu, weather=get_weather_main(),subtitle=subtitle)                

@seoul_bp.route('/crime/<path:path>')
def crime2(path):
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':1, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    path_dict = {'crime':'범죄','murder':'살인','rape':'강간','burglar':'강도','theft':'절도','violence':'폭력'}
    path2_dict = {'a_crime':'검거','a_murder':'살인검거율','a_rape':'강간검거율','a_burglar':'강도검거율','a_theft':'절도검거율','a_violence':'폭력검거율'}
    try:
        column_index = path_dict[path]
        subtitle = column_index
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11,
                tiles='Stamen Toner')
        map.choropleth(geo_data = geo_str,
                data = seoul_crime[column_index],
                columns = [seoul_crime.index, seoul_crime[column_index]],
                fill_color = 'PuRd',
                key_on = 'feature.id')
        map.save('templates/map.html')
    except:
        column_index2 = path2_dict[path]
        subtitle = column_index2
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11,
                tiles='Stamen Toner')
        map.choropleth(geo_data = geo_str,
                data = seoul_crime[column_index2],
                columns = [seoul_crime.index, seoul_crime[column_index2]],
                fill_color = 'PuRd',
                key_on = 'feature.id')
        for i in seoul_police.index:
            folium.CircleMarker([seoul_police.lat[i], seoul_police.lng[i]], radius=10,
                        tooltip=seoul_police['관서명'][i],
                        color='#3186cc', fill_color='#3186cc').add_to(map)
        map.save('templates/map.html')
     
    return render_template('seoul/crime.html', menu=menu, weather=get_weather_main(),subtitle=subtitle)  

@seoul_bp.route('/cctv',methods = ['GET'])
def cctv():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':1, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11,
                tiles='Stamen Toner')
    subject = request.args.get('subject','소계')
    map.choropleth(geo_data = geo_str,
            data = seoul_cctv[subject],
            columns = [seoul_cctv.index, seoul_cctv[subject]],
            fill_color = 'YlGnBu',
            key_on = 'feature.id')
    map.save('templates/map.html')
    return render_template('seoul/cctv.html', menu=menu, weather=get_weather_main(),subtitle=subject)
    
@seoul_bp.route('/cctv/grape',methods = ['GET'])
def cctv_grape():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':1, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    fp1 = np.polyfit(seoul_cctv['인구수'], seoul_cctv['소계'], 1)

    f1 = np.poly1d(fp1)
    fx = np.linspace(100000, 700000, 100)

    seoul_cctv['오차'] = np.abs(seoul_cctv['소계'] - f1(seoul_cctv['인구수']))

    df_sort = seoul_cctv.sort_values(by='오차', ascending=False)
    plt.figure(figsize=(8,6))
    plt.scatter(seoul_cctv['인구수'], seoul_cctv['소계'],c=seoul_cctv['오차'], s=50)
    plt.plot(fx, f1(fx), ls='dashed', lw=3, color='g')

    for n in range(10):
        plt.text(df_sort['인구수'][n]*1.02, df_sort['소계'][n]*0.98, df_sort.index[n] , fontsize=10)

    plt.xlabel('인구수')
    plt.ylabel('인구당 CCTV비율')

    plt.colorbar()
    plt.grid()
    img_file = os.path.join(current_app.root_path, 'static/img/cctv_grape.png')
    plt.savefig(img_file)
    mtime = int(os.stat(img_file).st_mtime)    
    return render_template('seoul/cctv_grape.html', menu=menu, weather=get_weather_main(),mtime=mtime)
