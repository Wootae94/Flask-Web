from flask import Blueprint, render_template,session,request
from flask import current_app, flash, url_for, redirect
from fbprophet import Prophet
from datetime import datetime, timedelta
import os
import pandas as pd
import pandas_datareader as pdr
import matplotlib as mpl 
from my_util.weather import get_weather

stock_bp = Blueprint('stock_bp', __name__)

kospi_dict, kosdaq_dict = {}, {}

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

@stock_bp.before_app_first_request
def before_app_first_request():
    kospi = pd.read_csv('./static/data/KOSPI.csv', dtype={'종목코드': str})
    for i in kospi.index:
        kospi_dict[kospi['종목코드'][i]] = kospi['기업명'][i]
    kosdaq = pd.read_csv('./static/data/KOSDAQ.csv', dtype={'종목코드': str})
    for i in kosdaq.index:
        kosdaq_dict[kosdaq['종목코드'][i]] = kosdaq['기업명'][i]

@stock_bp.route('/stock', methods=['GET', 'POST'])
def stock():
    menu = {'ho':0, 'da':1, 'ml':0, 'sc':0, 'co':0, 'ca':0, 'cr':0, 'st':1, 'wc':0}
    if request.method == 'GET':
        return render_template('stock/stock.html', menu=menu, weather=get_weather_main(),
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
        try:
            stock_data = pdr.DataReader(code, data_source='yahoo', start=start_learn,   end=end_learn)
            current_app.logger.debug(f"get stock data: {code}")
            df = pd.DataFrame({'ds': stock_data.index, 'y': stock_data.Close})
            df.reset_index(inplace=True)
            del df['Date']
        except:
            current_app.logger.error('Data error')
            flash(f'{company}_{code} 야후주식에 존재하지 않습니다.','danger')
            return redirect(url_for('stock_bp.stock'))

        mpl.use('Agg')

        model = Prophet(daily_seasonality=True)
        model.fit(df)
        future = model.make_future_dataframe(periods=pred_period)
        forecast = model.predict(future)
        fig = model.plot(forecast);
        img_file = os.path.join(current_app.root_path, 'static/img/stock.png')
        fig.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        return render_template('stock/stock_res.html', menu=menu, weather=get_weather_main(), 
                                mtime=mtime, company=company, code=code)
