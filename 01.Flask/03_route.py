from flask import Flask, render_template,request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flask'

@app.route('/user/<uid>')
def string_fn(uid):
    return uid

@app.route('/int/<int:number>')
def int_fn(number):
    return str(100*number)

@app.route('/float/<float:number>')
def float_fn(number):
    return str(10*number)

@app.route('/path/<path:path>')
def path_fn(path):
    return f'path : {path}'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return  render_template('03_loginForm.html') # 로그인 폼이 있는 창
    else:
        return  render_template('02_welcome.html') # 로그인 정보 받아서 처리

if __name__ == "__main__":
    app.run(debug=True)