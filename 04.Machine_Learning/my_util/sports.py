import time 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
def crawling(sports_target):
    driver = webdriver.Chrome('./static/data/chromedriver.exe')
    driver.maximize_window()
    result_text = ''
    for sport in sports_target:
        driver.get(f'https://sports.news.naver.com/{sport}/news/index.nhn?isphoto')
        while True:
            page = driver.find_element_by_id('_pageList')
            try:
                next = page.find_element_by_class_name('next')
                if next:
                    next.click()
            except:
                break
        last_paginate = driver.find_element_by_css_selector('.paginate')
        last_page = last_paginate.find_elements_by_tag_name('a')[-1].text
        for p in range(1,int(last_page)+1):
            driver.get(f'https://sports.news.naver.com/{sport}/news/index.nhn?isphoto=N&page={p}')
            time.sleep(2)
            news = driver.find_element_by_css_selector('.news_list')
            time.sleep(2)
            title_list = news.find_elements_by_css_selector('.title')
            time.sleep(1)
            for title in title_list:
                result_text += title.text
    driver.quit()
    return result_text