from flask import Flask, render_template, session, escape
from datetime import timedelta
from my_util.weather import get_weather
app = Flask(__name__)

app.secret_key = 'qwert12345'

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
@app.route('/')
def main():
    weather = get_weather()
    menu = {'ho':1, 'da':0, 'ml':0, 'sc':0, 'co':0, 'ca':0, 'cr':0, 'st':0, 'wc':0}
    return render_template('09_main.html',menu=menu,weather=get_weather_main())

if __name__ == "__main__":
    app.run(debug=True)