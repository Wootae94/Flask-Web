from flask import Blueprint, render_template, request, session, g
from flask import current_app
from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.datasets import load_digits
from sklearn.pipeline import Pipeline
import os, joblib
import pandas as pd
import matplotlib.pyplot as plt
from my_util.weather import get_weather

a_clf_bp = Blueprint('a_clf_bp', __name__)
menu = {'ho':0, 'da':0, 'ml':1, 'sc':0, 'co':0, 'ca':0, 'cr':0, 'wc':0, 'clf':0, 'a_clf':1, 'rg':0,'cl':0}

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
    weather = get_weather()
    return weather

@a_clf_bp.route('/digits', methods=['GET', 'POST'])
def digits():
    if request.method == 'GET':
        return render_template('advanced/digits.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        index_list = list(range(index, index+5))
        digits = load_digits()
        df = pd.read_csv('static/data/digits_test.csv')
        img_index_list = df['index'].values
        target_index_list = df['target'].values
        index_list = img_index_list[index:index+5]

        scaler = joblib.load('static/model/digits_scaler.pkl')
        test_data = df.iloc[index:index+5, 1:-1]
        test_scaled = scaler.transform(test_data)
        label_list = target_index_list[index:index+5]
        lrc = joblib.load('static/model/digits_lr.pkl')
        svc = joblib.load('static/model/digits_sv.pkl')
        rfc = joblib.load('static/model/digits_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)

        img_file_wo_ext = os.path.join(current_app.root_path, 'static/img/digit')
        for k, i in enumerate(index_list):
            plt.figure(figsize=(2,2))
            plt.xticks([]); plt.yticks([])
            img_file = img_file_wo_ext + str(k+1) + '.png'
            plt.imshow(digits.images[i], cmap=plt.cm.binary, interpolation='nearest')
            plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index_list, 'label':label_list,
                       'pred_lr':pred_lr, 'pred_sv':pred_sv, 'pred_rf':pred_rf}
        
        return render_template('advanced/digits_res.html', menu=menu, mtime=mtime,
                                result=result_dict, weather=get_weather())

@a_clf_bp.route('/mnist', methods=['GET', 'POST'])
def mnist():
    if request.method == 'GET':
        return render_template('advanced/mnist.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        index_list = list(range(index, index+3))
        df = pd.read_csv('static/data/mnist/mnist_test.csv')

        scaler = joblib.load('static/model/mnist_scaler.pkl')
        test_data = df.iloc[index:index+3, :-1].values
        test_scaled = scaler.transform(test_data)
        label_list = df.iloc[index:index+3, -1]
        svc = joblib.load('static/model/mnist_sv.pkl')
        pred_sv = svc.predict(test_scaled)

        img_file_wo_ext = os.path.join(current_app.root_path, 'static/img/mnist')
        for i in range(3):
            digit = test_data[i].reshape(28,28)
            plt.figure(figsize=(4,4))
            plt.xticks([]); plt.yticks([])
            img_file = img_file_wo_ext + str(i+1) + '.png'
            plt.imshow(digit, cmap=plt.cm.binary, interpolation='nearest')
            plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index_list, 'label':label_list, 'pred_sv':pred_sv,}
        
        return render_template('advanced/mnist_res.html', menu=menu, mtime=mtime,
                                result=result_dict, weather=get_weather())

@a_clf_bp.route('/imdb', methods=['GET', 'POST'])
def imdb():
    imdb_count_lr = joblib.load('static/model/imdb_count_lr.pkl')
    imdb_tfidf_lr = joblib.load('static/model/imdb_tfidf_lr.pkl')
    if request.method == 'GET':
        return render_template('advanced/imdb.html', menu=menu, weather=get_weather())
    else:
        test_data = []
        label = '직접 확인'
        if request.form['option'] == 'index':
            index = int(request.form['index'] or '0')
            df_test = pd.read_csv('static/data/IMDB_test.csv')
            test_data.append(df_test.iloc[index, 0])
            label = '긍정' if df_test.sentiment[index] else '부정'
        else:
            test_data.append(request.form['review'])

        pred_cl = '긍정' if imdb_count_lr.predict(test_data)[0] else '부정'
        pred_tl = '긍정' if imdb_tfidf_lr.predict(test_data)[0] else '부정'
        result_dict = {'label':label, 'pred_cl':pred_cl, 'pred_tl':pred_tl}
        return render_template('advanced/imdb_res.html', menu=menu, review=test_data[0],
                                res=result_dict, weather=get_weather())

@a_clf_bp.route('/naver', methods=['GET', 'POST'])
def naver():
    if request.method == 'GET':
        pass
    else:
        pass

@a_clf_bp.route('/news', methods=['GET', 'POST'])
def news():
    news_count_lr = joblib.load('static/model/news_count_lr.pkl')
    news_tfidf_lr = joblib.load('static/model/news_tfidf_lr.pkl')
    news_tfidf_sv = joblib.load('static/model/news_tfidf_sv.pkl')
    target_names = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc',
                    'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x',
                    'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
                    'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med',
                    'sci.space', 'soc.religion.christian', 'talk.politics.guns',
                    'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc']
    if request.method == 'GET':
        return render_template('advanced/news.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        df = pd.read_csv('static/data/news/test.csv')
        label = f'{df.target[index]} ({target_names[df.target[index]]})'
        test_data = []
        test_data.append(df.data[index])

        pred_c_lr = news_count_lr.predict(test_data)
        pred_t_lr = news_tfidf_lr.predict(test_data)
        pred_t_sv = news_tfidf_sv.predict(test_data)
        result_dict = {'index':index, 'label':label, 
                       'pred_c_lr':f'{pred_c_lr[0]} ({target_names[pred_c_lr[0]]})',
                       'pred_t_lr':f'{pred_t_lr[0]} ({target_names[pred_t_lr[0]]})',
                       'pred_t_sv':f'{pred_t_sv[0]} ({target_names[pred_t_sv[0]]})'}
        
        return render_template('advanced/news_res.html', menu=menu, news=df.data[index],
                                res=result_dict, weather=get_weather())