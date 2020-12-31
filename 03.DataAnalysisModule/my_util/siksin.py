from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pandas as pd

def get_siksinhot_res(region_num):
    img_list,title_list,region_list = [],[],[]
    sector_list,intro_list,phone_list = [],[],[]
    address_list,road_list,time_list,homepage_list = [],[],[],[]
    sido_list = []
    url_list = []
    url_base = 'https://www.siksinhot.com'
    url_sub =  f'/taste?upHpAreaId={region_num}&hpAreaId=&isBestOrd=Y'
    url = url_base + url_sub
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/630.3239.132 Safari/537.36'}
    req = requests.get(url, headers = headers)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    res_list = soup.select_one('.listTy1').find_all('li')
    for i in range(len(res_list)):
        try:
            img = res_list[i].find('img').get('src')
            title = res_list[i].select_one('.store').get_text()
            res_url = res_list[i].find('a').get('href')
            new_url = url_base + res_url
            new_req = requests.get(new_url, headers = headers)
            new_html = new_req.text
            new_soup = BeautifulSoup(new_html, 'html.parser') 
            region = new_soup.select_one('.store_info').find_all('p')[0].get_text()
            intro = new_soup.select_one('.store_info').find_all('p')[2].get_text()
            address = ' '.join(new_soup.select_one('.store_info').find_all('p')[4].find('a').get_text().split()[1:])
            url_list.append(new_url)
            img_list.append(img)
            title_list.append(title)
            region_list.append(region)
            intro_list.append(intro)
            address_list.append(address)
        except:
            pass
    df = pd.DataFrame({
                        'url':url_list,
                        '식당명':title_list,
                        '이미지':img_list,
                        '소개':intro_list,
                        '주소':address_list})
                        
    params_list = []
    for i in df.index:    
        params=[]
        params = [df['url'][i],df['식당명'][i],df['이미지'][i],df['소개'][i],df['주소'][i]]
        params_list.append(params)
    return params_list
