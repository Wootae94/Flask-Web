from flask import Flask, render_template, session, request
from fbprophet import Prophet
from datetime import datetime, timedelta
import os, json, folium, logging
from logging.config import dictConfig
import pandas as pd
import pandas_datareader as pdr
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from matplotlib import rc

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

from my_util.weather import get_weather
app = Flask(__name__)
app.secret_key = 'qwert12345'
kospi_dict, kosdaq_dict = {}, {}

with open('./logging.json','r') as file:
    config = json.load(file)
dictConfig(config)
app.logger

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

@app.before_first_request
def before_first_request():
    kospi = pd.read_csv('./static/data/KOSPI.csv', dtype={'종목코드': str})
    for i in kospi.index:
        kospi_dict[kospi['종목코드'][i]] = kospi['기업명'][i]
    kosdaq = pd.read_csv('./static/data/KOSDAQ.csv', dtype={'종목코드': str})
    for i in kosdaq.index:
        kosdaq_dict[kosdaq['종목코드'][i]] = kosdaq['기업명'][i]

@app.before_request
def before_request():
    pass    # 모든 Get 요청을 처리하는 놈에 앞서서 공통적으로 뭔 일을 처리함

@app.route('/')
def index():
    menu = {'ho':1, 'da':0, 'ml':0, 'sc':0, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    return render_template('main.html', menu=menu, weather=get_weather_main())

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/park', methods=['GET', 'POST'])
def park():
    seoul_park = pd.read_csv('./static/data/Seoul_Park.csv')
    park_list = seoul_park['공원명'].tolist()
    gu_park = pd.read_csv('./static/data/gu_park.csv')
    gu_list = gu_park['지역구'].tolist()
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':1, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    if request.method == 'GET':
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
        for i in seoul_park.index:
            folium.CircleMarker([seoul_park.lat[i], seoul_park.lng[i]], 
                        radius=int(seoul_park['반지름'][i]*3),
                        tooltip=f"{seoul_park['공원명'][i]}({int(seoul_park['면적'][i])}㎡)",
                        color='#3186cc', fill_color='#3186cc').add_to(map)
        map.save('templates/map.html')
        return render_template('park.html', menu=menu, weather=get_weather_main(), park_list=park_list, gu_list=gu_list)
    else:
        gubun = request.form['gubun']
        app.logger.info(gubun)
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
            return render_template('park_res.html', menu=menu, weather=get_weather_main(), park_select=park_select)
        else:
            seoul_gu = request.form['seoul_gu']
            df = seoul_park[seoul_park['지역구']==seoul_gu].reset_index(drop=True)
            df2 = gu_park[gu_park['지역구']==seoul_gu].reset_index(drop=True)
            gu_select = df2.loc[0,:].tolist()
            park_mean = gu_park.mean().round(2).tolist()
            map = folium.Map(location=[df.lat.mean(),df.lng.mean()], zoom_start=11)
            for i in df.index:
                folium.CircleMarker([df.lat[i], df.lng[i]], 
                            radius=int(df['반지름'][i]*3),
                            tooltip=f"{df['공원명'][i]}({int(df['면적'][i])}㎡)",
                            color='#3186cc', fill_color='#3186cc').add_to(map)
            map.save('templates/map.html')
            return render_template('park_res2.html', menu=menu, weather=get_weather_main(),gu_select=gu_select,park_mean=park_mean)                

@app.route('/park_gu')
def park_gu():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':1, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    seoul_park = pd.read_csv('./static/data/Seoul_Park.csv')
    subtitle = '공원 위치와 크기'
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Stamen Toner')
    for i in seoul_park.index:
        folium.CircleMarker([seoul_park.lat[i], seoul_park.lng[i]], 
                            radius=int(seoul_park['반지름'][i]),
                            tooltip=f"{seoul_park['공원명'][i]}({int(seoul_park['면적'][i])}㎡)",
                            color='green', fill_color='green').add_to(map)
    map.save('templates/map.html')
    return render_template('park_gu.html', menu=menu, weather=get_weather_main(),subtitle=subtitle)                

@app.route('/park_gu/<path:path>')
def park_gu2(path):
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':1, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    gu_park = pd.read_csv('./static/data/gu_park.csv')
    gu_park.set_index('지역구',inplace=True)
    geo_path = './static/data/skorea_municipalities_geo_simple.json'
    geo_str = json.load(open(geo_path, encoding='utf8'))
    if path == 'area':
        subtitle = '자치구별 공원총면적'
        map = folium.Map(location=[37.55277229023488, 126.99057136537], zoom_start=11,
                tiles='Stamen Toner')
        map.choropleth(geo_data = geo_str,
                        data = gu_park['공원총면적'],
                        columns = [gu_park.index,gu_park['공원총면적']],
                        fill_color = 'PuRd',
                        key_on = 'feature.id')
        loc = 'Corpus Christi'
        map.save('templates/map.html')
        return render_template('park_gu.html', menu=menu, weather=get_weather_main(),subtitle=subtitle)                
    if path == 'area_ratio':
        subtitle = '자치구별 공원면적비'
        map = folium.Map(location=[37.55277229023488, 126.99057136537], zoom_start=11,
                tiles='Stamen Toner')
        map.choropleth(geo_data = geo_str,
                        data = gu_park['면적비'],
                        columns = [gu_park.index,gu_park['면적비']],
                        fill_color = 'PuRd',
                        key_on = 'feature.id')
        loc = 'Corpus Christi'
        map.save('templates/map.html')
        return render_template('park_gu.html', menu=menu, weather=get_weather_main(),subtitle=subtitle)   
    if path == 'per_person':
        subtitle = '자치구별 1인당 공원면적'
        map = folium.Map(location=[37.55277229023488, 126.99057136537], zoom_start=11,
                tiles='Stamen Toner')
        map.choropleth(geo_data = geo_str,
                        data = gu_park['인구수당면적'],
                        columns = [gu_park.index,gu_park['인구수당면적']],
                        fill_color = 'PuRd',
                        key_on = 'feature.id')
        loc = 'Corpus Christi'
        map.save('templates/map.html')
        return render_template('park_gu.html', menu=menu, weather=get_weather_main(),subtitle=subtitle)   
    if path == 'number':
        subtitle = '자치구별 공원수'
        map = folium.Map(location=[37.55277229023488, 126.99057136537], zoom_start=11,
                tiles='Stamen Toner')
        map.choropleth(geo_data = geo_str,
                        data = gu_park['공원 갯수'],
                        columns = [gu_park.index,gu_park['공원 갯수']],
                        fill_color = 'PuRd',
                        key_on = 'feature.id')
        loc = 'Corpus Christi'
        map.save('templates/map.html')
        return render_template('park_gu.html', menu=menu, weather=get_weather_main(),subtitle=subtitle)   

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':0, 'ca':0, 'cr':0, 'st':1, 'wc':0}
    if request.method == 'GET':
        return render_template('stock.html', menu=menu, weather=get_weather_main(),
                                kospi=kospi_dict, kosdaq=kosdaq_dict)
    else:
        market = request.form['market']
        if market == 'KS':
            code = request.form['kospi_code']
            company = kospi_dict[code]
            code += '.KS'
        else:
            code = request.form['kosdaq_code']
            company = kosdaq_dict[code]
            code += '.KQ'
        learn_period = int(request.form['learn'])
        pred_period = int(request.form['pred'])
        today = datetime.now()
        start_learn = today - timedelta(days=learn_period*365)
        end_learn = today - timedelta(days=1)

        stock_data = pdr.DataReader(code, data_source='yahoo', start=start_learn, end=end_learn)
        app.logger.debug(f"get stock data: {code}")
        df = pd.DataFrame({'ds': stock_data.index, 'y': stock_data.Close})
        df.reset_index(inplace=True)
        try:
            del df['Date']
        except:
            pass
        mpl.use('Agg')

        model = Prophet(daily_seasonality=True)
        model.fit(df)
        future = model.make_future_dataframe(periods=pred_period)
        forecast = model.predict(future)
        fig = model.plot(forecast);
        img_file = os.path.join(app.root_path, 'static/img/stock.png')
        fig.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        return render_template('stock_res.html', menu=menu, weather=get_weather_main(), 
                                mtime=mtime, company=company, code=code)

if __name__ == '__main__':
    app.run(debug=True)