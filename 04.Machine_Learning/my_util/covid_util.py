import requests
from urllib.parse import urlparse,quote
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import db.db_module as dm
import matplotlib as mpl 
import matplotlib.pyplot as plt
from flask import current_app
import os
import seaborn as sns
import datetime

def new_covid_daily(date):
    key_fd = open('./static/data/covid19apikey.txt', mode='r')
    api_key = key_fd.read(100)
    key_fd.close()

    createDt_list,deathCnt_list,defCnt_list,gubun_list,incDec_list = [],[],[],[],[]
    isolClearCnt_list,isolIngCnt_list,localOccCnt_list,overFlowCnt_list = [],[],[],[]
    qurRate_list,seq_list,stdDay_list,updateDt_list = [],[],[],[]

    page = 1
    corona_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
    url = f'{corona_url}?ServiceKey={api_key}&pageNo={page}&numOfRows=10&startCreateDt={date}&endCreateDt={date}'
    result = requests.get(url)
    soup = BeautifulSoup(result.text,'xml')
    items = soup.find_all('item')
    
    for item in items:
        createDt_list.append(item.find('createDt').string if item.find('createDt') else 0)
        deathCnt_list.append(item.find('deathCnt').string if item.find('deathCnt') else 0)
        defCnt_list.append(item.find('defCnt').string if item.find('defCnt') else 0)
        gubun_list.append(item.find('gubun').string if item.find('gubun') else '')
        incDec_list.append(item.find('incDec').string if item.find('incDec') else 0)
        isolClearCnt_list.append(item.find('isolClearCnt').string if item.find('isolClearCnt') else 0)
        isolIngCnt_list.append(item.find('isolIngCnt').string if item.find('isolIngCnt') else 0)
        localOccCnt_list.append(item.find('localOccCnt').string if item.find('localOccCnt') else 0)
        overFlowCnt_list.append(item.find('overFlowCnt').string if item.find('overFlowCnt') else 0)
        qurRate_list.append(item.find('qurRate').string if item.find('qurRate') else 0)
        seq_list.append(item.find('seq_list').string if item.find('seq_list') else '')
        stdDay_list.append(item.find('stdDay').string if item.find('stdDay') else '')
        updateDt_list.append(item.find('updateDt').string if item.find('updateDt') else '')

    df = pd.DataFrame({
        '등록시간':createDt_list, '사망자':deathCnt_list, '확진자':defCnt_list,
        '광역시도':gubun_list, '전일대비':incDec_list, '격리해제':isolClearCnt_list, 
        '격리중':isolIngCnt_list, '지역발생':localOccCnt_list,'해외유입':overFlowCnt_list,
        '10만명당':qurRate_list, 'ID':seq_list, '기준시간':stdDay_list, '수정시간':updateDt_list
    })
    df = df[df.index<=18]
    year_list,mounth_list,day_list = [],[],[]
    for i in df.index:
        tmp_list = re.findall("\d+",df['기준시간'][i])
        year_list.append(tmp_list[0])
        mounth_list.append(tmp_list[1])
        day_list.append(tmp_list[2])
    date_list=[]
    for i in df.index:
        tmp_date = year_list[i]+'-'+mounth_list[i]+'-'+day_list[i]
        date_list.append(tmp_date)
    df['기준시간'] = date_list
    df.fillna(0,inplace=True)
    df.reset_index(drop=True,inplace=True)
    df=df[['기준시간','광역시도','사망자','확진자','전일대비','격리해제','격리중','지역발생','해외유입','10만명당']]
    for i in df.index:    
        params=[]
        params = [df['기준시간'][i], int(df['사망자'][i]), int(df['확진자'][i]), 
                  df['광역시도'][i], int(df['전일대비'][i]), int(df['격리해제'][i]), 
                  int(df['격리중'][i]), int(df['지역발생'][i]), int(df['해외유입'][i])]
        params.append(None if df['10만명당'][i].find('-')>-1 else float(df['10만명당'][i]))
        
        dm.write_covid_daily(params)

def new_covid_agender(date):
    key_fd = open('./static/data/covid19genderkey.txt', mode='r')
    api_key = key_fd.read(100)
    key_fd.close()
    
    gubun_list,confCase_list,confCaseRate_list,death_list,deathRate_list = [],[],[],[],[]
    criticalRate_list,createDt_list,updateDt_list = [],[],[]

    page = 1
    corona_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19GenAgeCaseInfJson'
    url = f'{corona_url}?ServiceKey={api_key}&pageNo={page}&numOfRows=10&startCreateDt={date}&endCreateDt={date}'
    result = requests.get(url)
    soup = BeautifulSoup(result.text,'xml')
    items = soup.find_all('item')

    for item in items:
        gubun_list.append(item.find('gubun').string if item.find('gubun') else '')
        confCase_list.append(item.find('confCase').string if item.find('confCase') else 0)
        confCaseRate_list.append(item.find('confCaseRate').string if item.find('confCaseRate') else 0)
        death_list.append(item.find('death').string if item.find('death') else '')
        deathRate_list.append(item.find('deathRate').string if item.find('deathRate') else 0)
        criticalRate_list.append(item.find('criticalRate').string if item.find('criticalRate') else 0)
        createDt_list.append(item.find('createDt').string if item.find('createDt') else 0)
        updateDt_list.append(item.find('updateDt').string if item.find('updateDt') else 0)

    df = pd.DataFrame({
        '구분':gubun_list, '확진자':confCase_list, '확진률':confCaseRate_list,
        '사망자':death_list, '사망률':deathRate_list, '치명률':criticalRate_list, 
        '등록일자':createDt_list, '수정일자':updateDt_list
    })
    del df['수정일자']
    df['등록일자'] = df['등록일자'].str[0:10]
    for i in range(len(df)):
        params = [df.iloc[i,-1],df.iloc[i,0]]
        for k in range(1,6):
            params.append(df.iloc[i,k])
        dm.write_covid_agender(params)

def new_covid_region(date):    
    key_fd = open('./static/data/covid19apikey.txt', mode='r')
    govapi_key = key_fd.read(100)
    key_fd.close()
    target_date = ''.join(date.split('-'))
    dict_list=[]
    raw_dict = {'날짜': date,'제주':0, '경남':0,'경북':0,'전남':0,'전북':0,'충남':0,'충북':0,'강원':0,'경기':0,'세종':0,'울산':0,   '대전':0,'광주':0,'인천':0,'대구':0,'부산':0,'서울':0}
    page = 1
    corona_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
    url = f'{corona_url}?ServiceKey={govapi_key}&pageNo={page}&numOfRows=10&startCreateDt={target_date}&endCreateDt={target_date}'
    result = requests.get(url)
    soup = BeautifulSoup(result.text,'xml')
    items = soup.find_all('item')
    for k in range(len(items)):
        raw_dict[items[k].find('gubun').get_text()] = items[k].find('incDec').get_text()
    dict_list.append(raw_dict)
    df = pd.DataFrame(dict_list)
    for i in range(len(df)):
        params=[df['날짜'][i],df['제주'][i],df['경남'][i],df['경북'][i],df['전남'][i],df['전북'][i],df['충남'][i],df['충북'][i],df['강원'][i],df['경기'][i],df['세종'][i],df['울산'][i],df['대전'][i],df['광주'][i],df['인천'][i],df['대구'][i],df['부산'][i],df['서울'][i],df['합계'][i]]
        dm.write_covid_region(params)

def draw_seoul_line(gu_list,date_list):
    corona_seoul = pd.read_csv('./static/data/서울코로나.csv')
    corona_seoul['확진일'] = pd.to_datetime(corona_seoul['확진일'])
    corona_seoul_select = corona_seoul[datetime.datetime.strptime(date_list[1],'%Y-%m-%d')>corona_seoul['확진일']][corona_seoul['확진일']>datetime.datetime.strptime(date_list[0],'%Y-%m-%d')]
    corona_seoul_select.reset_index(drop=True,inplace=True)

    col_list = corona_seoul_select.columns[1:]
    x_index = corona_seoul_select['확진일']
    
    plt.figure(figsize=(20,15))
    count = corona_seoul_select['확진일'].count()
    for gu in gu_list:
        plt.plot(x_index ,corona_seoul_select[gu], '-',label=gu); 
    plt.xticks(fontsize=20, rotation=45)
    plt.yticks(fontsize=20)
    plt.legend(fontsize=20)
    plt.grid()
    
    img_file = os.path.join(current_app.root_path, 'static/img/seoul_trend.png')
    plt.savefig(img_file)
    mtime = int(os.stat(img_file).st_mtime)
    result = [col_list,mtime]
    return(result)

def draw_seoul_bar(subject):
    corona_gu = pd.read_csv('./static/data/구별 코로나.csv',index_col='지역')
    gu_colona_sort = corona_gu.sort_values(by=subject,ascending=False)
    gu_colona_sort.reset_index(inplace=True)
    plt.figure(figsize=(20,15))
    sns.barplot(data=gu_colona_sort,x=gu_colona_sort['지역'],y=gu_colona_sort[subject])
    plt.xlabel('확진자 수',fontsize=20)
    plt.ylabel(subject,fontsize=20)
    plt.xticks(fontsize=20,rotation=45)
    plt.yticks(fontsize=20)
    plt.legend(fontsize=20)
    img_file = os.path.join(current_app.root_path, 'static/img/seoul_compare.png')
    plt.savefig(img_file)
    mtime = int(os.stat(img_file).st_mtime)    
    return mtime
    