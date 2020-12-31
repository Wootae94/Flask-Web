from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import requests
def get_melon_top_100():
    url ='https://www.melon.com/chart/week/index.htm'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132   Safari/537.36'}
    req = requests.get(url, headers = headers)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    date = soup.select_one('.yyyymmdd').get_text().strip()
    start_day = date[:10]
    end_day = date[13:]
    ranks = []; diffs = []; 
    titles = []; singers = []; albums = []
    images = []; hrefs = []
    url_tmp = 'https://www.melon.com/album/detail.htm?albumId='
    service_list = soup.select_one('.service_list_song')
    tbody = service_list.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:
        rank = int(tr.select_one('.rank').string)
        image = tr.find('img').get('src') 
        href = url_tmp + tr.find('a').get('href').split("'")[1]
        info = tr.select_one('.ellipsis.rank01')
        title = info.find('a').string
        info = tr.select_one('.ellipsis.rank02')
        singer = info.find('a').string
        info = tr.select_one('.ellipsis.rank03')
        album = info.find('a').string
        entry = tr.select_one('.rank_wrap')
        spans = entry.find_all('span')
        diff = -100
        if len(spans) == 3:
            diff = int(spans[2].string)
            if diff != 0:
                sign = spans[2].attrs['class']
                if sign[0] == 'down':
                    diff *= -1
        ranks.append(rank)
        images.append(image)
        hrefs.append(href)
        diffs.append(diff)    
        titles.append(title)        
        singers.append(singer)
        albums.append(album)
    Melon_top_100 = pd.DataFrame({
                     'rank' : ranks,
                     'image':images,
                     'href':hrefs,
                     'diff' : diffs,
                     'title' : titles,
                     'singer' : singers,
                     'album' : albums
                     })
    params_list = []
    for i in Melon_top_100.index:    
        params=[]
        params = [Melon_top_100['rank'][i],Melon_top_100['image'][i],Melon_top_100['href'][i],Melon_top_100['diff'][i],Melon_top_100['title'][i],Melon_top_100['singer'][i],   Melon_top_100['album'][i]]
        params_list.append(params)

    return params_list