
from flask import Blueprint, render_template, session,request
import folium
import pandas as pd
import json
from datetime import datetime, timedelta
from my_util.weather import get_weather
from my_util.siksin import get_siksinhot_res
from my_util.melon import get_melon_top_100
from my_util.yes24 import get_yes24_best
from flask import current_app
import numpy as np
import matplotlib as mpl 
import matplotlib.pyplot as plt
import os
crawling_bp = Blueprint('crawling_bp', __name__)

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

@crawling_bp.route('/restaurant', methods=['GET', 'POST'])
def restaurant():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':0, 'ca':0, 'cr':1, 'st':0, 'wc':0}
    if request.method == 'GET':
        region_list = ['서울-강남','서울-강북','경기','인천','부산','대구','광주','대전','울산','강원','경남','경북','전남','전북','충남','충북','제주']
        
        return render_template('crawling/restaurant.html', menu=menu, weather=get_weather(),region_list=region_list)
    else:
        region_dict = {'서울-강남':'9','서울-강북':'10','경기':'2','인천':'12','부산':'8','대구':'6','광주':'5','대전':'7','울산':'11','강원':'1','경남':'3','경북':'4','전남':'13','전북':'14','충남':'16','충북':'17','제주':'15'}
        region = request.form['region']
        current_app.logger.info(region)
        region_num = region_dict[region]
        current_app.logger.info(region_num)
        params_list = get_siksinhot_res(region_num)
        return render_template('crawling/restaurant_res.html', menu=menu, weather=get_weather(),params_list=params_list,region=region)

@crawling_bp.route('/music',methods=['GET'])
def music():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':0, 'ca':0, 'cr':1, 'st':0, 'wc':0}
    params_list = get_melon_top_100()
    
    return render_template('crawling/music.html', menu=menu, weather=get_weather(),params_list=params_list)

@crawling_bp.route('/book',methods=['GET'])
def book():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':0, 'ca':0, 'cr':1, 'st':0, 'wc':0}
    
    params_list = get_yes24_best()
    return render_template('crawling/book.html', menu=menu, weather=get_weather(),params_list=params_list)
    