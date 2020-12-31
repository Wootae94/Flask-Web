from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import requests
def get_yes24_best():
    titles,writers,publishers,prices,intros,hrefs = [],[],[],[],[],[]
    for p in range(10):    
        page = p
        url_base = 'http://www.yes24.com'
        url_sub =  f'/24/category/bestseller?CategoryNumber=001&sumgb=06&PageNumber={page}'
        url = url_base + url_sub
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132   Safari/537. 36'}
        req = requests.get(url, headers = headers)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')
        for i in range(0,40,2):
            title = trs[i].select_one('.goodsTxtInfo').find_all('a')[0].get_text()
            writer = trs[i].select_one('.goodsTxtInfo').find_all('a')[2].get_text()
            publisher = trs[i].select_one('.goodsTxtInfo').find_all('a')[3].get_text()
            price = trs[i].select_one('.priceB').get_text()
            href = url_base + trs[i].select_one('.goodsTxtInfo').find_all('a')[0].get('href')
            try:
                intro = trs[i+1].select_one('.read').get_text().strip().split('.')[0]
            except:
                intro = ''
            titles.append(title)
            writers.append(writer)
            publishers.append(publisher)
            prices.append(price)
            hrefs.append(href)
            intros.append(intro)
    yes24_df = pd.DataFrame({'제목':titles,'저자':writers,'출판사':publishers,'가격':prices,'소개':intros,'href':hrefs})
    params_list = []
    for i in yes24_df.index:    
        params=[]
        params = [yes24_df['제목'][i],yes24_df['저자'][i],yes24_df['출판사'][i],yes24_df['가격'][i],yes24_df['소개'][i],yes24_df['href'][i]]
        params_list.append(params)
    
    return params_list