from flask import Flask, render_template, session, request
from fbprophet import Prophet
from datetime import datetime, timedelta
import os, json, folium, logging
from logging.config import dictConfig
from bp.simple import simple_bp
from bp5_stock.stock import stock_bp
from bp1_seoul.seoul import seoul_bp
from bp3_carto.carto import carto_bp
from my_util.weather import get_weather
app = Flask(__name__)
app.secret_key = 'qwert12345'
app.config['SESSION_COOKIE_PATH'] = '/'
app.register_blueprint(simple_bp, url_prefix = '/simple')
app.register_blueprint(stock_bp, url_prefix = '/stock')
app.register_blueprint(seoul_bp, url_prefix = '/seoul')
app.register_blueprint(carto_bp, url_prefix = '/carto')

with open('./logging.json','r') as file:
    config = json.load(file)
dictConfig(config)


def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        app.logger.debug("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)
    return weather

@app.route('/')
def index():
    menu = {'ho':1, 'da':0, 'ml':0, 'sc':0, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    return render_template('main.html', menu=menu, weather=get_weather_main())

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)