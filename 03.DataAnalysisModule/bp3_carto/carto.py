from flask import Blueprint, render_template, request, session
from flask import current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import timedelta
import os, folium, json
import pandas as pd
from my_util.weather import get_weather
import my_util.drawKorea as dK

carto_bp = Blueprint('carto_bp', __name__)

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

@carto_bp.route('/coffee', methods=['GET', 'POST'])
def coffee():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':0, 'ca':1, 'cr':0, 'st':0, 'wc':0}
    if request.method == 'GET':
        return render_template('cartogram/coffee.html', menu=menu, weather=get_weather_main())
    else:
        item = request.form['item']
        current_app.logger.debug(f"get data: {item}")
        try:
            f = request.files['csv']
            # filename = os.path.join(current_app.root_path, 'static/upload/') + secure_filename(f.filename)
            filename = os.path.join(current_app.root_path, 'static/upload/') + f.filename
            f.save(filename)
            current_app.logger.info(f'{filename} is saved.')
            df_coffee = pd.read_csv(filename, dtype={'빽다방 매장수':int,'커피빈 매장수':int,'스타벅스 매장수':int,'이디야 매장수':int})
            img_path = current_app.root_path
            current_app.logger.debug(f"get data: {img_path}")
            color_dict = {'커피지수':'Blues','빽다방 매장수':'Reds','커피빈 매장수':'Greens', '스타벅스 매장수':'PuBu','이디야  매장수':'Purples'}
            color = color_dict[item]
            img_file = dK.drawKorea(item, df_coffee, color, img_path)
            current_app.logger.debug(f"get data: {img_file}")
            mtime = int(os.stat(img_file).st_mtime)

            df_coffee_sort = df_coffee.sort_values(by=[item],ascending=False)[['ID',item]].reset_index().head(10)
            top10 = {}
            for i in range(10):
                top10[df_coffee_sort['ID'][i]] = round(df_coffee_sort[item][i], 2)
            subtitle = item
        except:
            current_app.logger.error('Data error')
            flash('csv 파일을 선택해주세요','danger')
            return redirect(url_for('carto_bp.coffee'))
        return render_template('cartogram/coffee_res.html', menu=menu, weather=get_weather_main(),mtime=mtime,subtitle=subtitle,top10=top10)

@carto_bp.route('/pop', methods=['GET', 'POST'])
def pop():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':0, 'ca':1, 'cr':0, 'st':0, 'wc':0}
    if request.method == 'GET':
        return render_template('cartogram/pop.html', menu=menu, weather=get_weather_main())
    else:
        item = request.form['item']
        current_app.logger.debug(f"get data: {item}")
        try:
            f = request.files['csv']
            # filename = os.path.join(current_app.root_path, 'static/upload/') + secure_filename(f.filename)
            filename = os.path.join(current_app.root_path, 'static/upload/') + f.filename
            f.save(filename)
            current_app.logger.info(f'{filename} is saved.')
            df_pop = pd.read_csv(filename)
            img_path = current_app.root_path
            current_app.logger.debug(f"get data: {img_path}")
            color_dict = {'인구수계':'Blues','소멸위기지역':'Reds','소멸비율':'Oranges','여성비':'Greens', '2030여성비':'PuRd'}
            color = color_dict[item]
            img_file = dK.drawKorea(item, df_pop, color, img_path)
            current_app.logger.debug(f"get data: {img_file}")
            mtime = int(os.stat(img_file).st_mtime)

            df_pop_sort = df_pop.sort_values(by=[item],ascending=False)[['ID',item]].reset_index().head(10)
            top10 = {}
            for i in range(10):
                top10[df_pop_sort['ID'][i]] = round(df_pop_sort[item][i], 2)
            subtitle = item
        except:
            current_app.logger.error('Data error')
            flash('csv 파일을 선택해주세요','danger')
            return redirect(url_for('carto_bp.pop'))
        return render_template('cartogram/pop_res.html', menu=menu, weather=get_weather_main(),mtime=mtime,subtitle=subtitle,top10=top10)


@carto_bp.route('/burger', methods=['GET', 'POST'])
def burger():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':0, 'ca':1, 'cr':0, 'st':0, 'wc':0}
    if request.method == 'GET':
        return render_template('cartogram/burger.html', menu=menu, weather=get_weather_main())
    else:
        item = request.form['item']
        current_app.logger.debug(f"get data: {item}")
        try:
            f = request.files['csv']
            # filename = os.path.join(current_app.root_path, 'static/upload/') + secure_filename(f.filename)
            filename = os.path.join(current_app.root_path, 'static/upload/') + f.filename
            f.save(filename)
            current_app.logger.info(f'{filename} is saved.')

            df_burger = pd.read_csv(filename, dtype= {'롯데리아 매장수':int,'맘스터치 매장수':int,'버거킹 매장수':int,'맥도날드 매장수':int,    'KFC 매장수':int})
            img_path = current_app.root_path
            current_app.logger.debug(f"get data: {img_path}")
            color_dict = {'버거지수':'Blues','롯데리아 매장수':'Reds','맘스터치 매장수':'Greens', '버거킹 매장수':'PuRd','맥도날드  매장수':'Purples','KFC 매장수':'Oranges'}
            color = color_dict[item]
            img_file = dK.drawKorea(item, df_burger, color, img_path)
            current_app.logger.debug(f"get data: {img_file}")
            mtime = int(os.stat(img_file).st_mtime)

            df_burger_sort = df_burger.sort_values(by=[item],ascending=False)[['ID',item]].reset_index().head(10)
            top10 = {}
            for i in range(10):
                top10[df_burger_sort['ID'][i]] = round(df_burger_sort[item][i], 2)
            subtitle = item
        except:
            current_app.logger.error('Data error')
            flash('csv 파일을 선택해주세요','danger')
            return redirect(url_for('carto_bp.burger'))
        return render_template('cartogram/burger_res.html', menu=menu, weather=get_weather_main(),mtime=mtime,subtitle=subtitle,top10=top10)