import requests
from urllib.parse import urlparse
def get_weather():
    key_fd = open('../static/data/openweatherkey.txt', mode='r')
    api_key = key_fd.read(100)
    key_fd.close()
    
    lat = 37.5509655144007
    lng = 126.849532173376
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}&units=metric&lang=kr'
    x = requests.get(urlparse(url).geturl()).json()
    y = x["main"] 
    temp = y["temp"] 
    temp_min = round(y['temp_min']-0.01,1)
    temp_max = round(y['temp_max']-0.01,1)
    z = x["weather"] 
    icon_code = z[0]["icon"] 
    icon_url = f'http://openweathermap.org/img/w/{icon_code}.png'
    desc = z[0]["description"] 
    return f'<img src={icon_url} alt="weather_icon" height = 32> <strong>{desc}</strong> 온도: <strong>{temp}\u00b0</strong> {temp_min}/{temp_max}\u00b0'