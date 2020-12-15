from flask import Flask, render_template,request
from flask import Response, make_response
app = Flask(__name__)

@app.route('/area')
def area():
    pi = request.args.get('pi','3.14') # pi값이 주어지지 않으면 3.14
    radius = request.values['radius'] # values로 하면 자동으로 처리
    s = float(pi)*float(radius)*float(radius)
    return f'pi = {pi}, radius = {radius}, area = {s}'


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return  render_template('03_loginForm.html') # 로그인 폼이 있는 창
    else:
        uid = request.form['uid']
        pwd = request.values['pwd']
        return f'uid = {uid}, pwd = {pwd}'

@app.route('/response')
def response_fn():
    custom_res = Response('Custom Response', 200, {'text':'ttt'})
    return make_response(custom_res)
    
if __name__ == "__main__":
    app.run(debug=True)