import time 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
def crawling(sports_target):
    driver = webdriver.Chrome('./static/data/chromedriver.exe')
    driver.maximize_window()
    result_text = ''
    for sport in sports_target:
        driver.get(f'https://sports.news.naver.com/{sport}/news/index.nhn?isphoto')
        page = len(driver.find_element_by_css_selector('.paginate').text.split())
        for p in range(1,page+1):
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