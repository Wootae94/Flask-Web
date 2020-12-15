from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def carousel():
    return render_template('08_carousel.html')

@app.route('/table')
def table():
    return render_template('08_table.html')
if __name__ == "__main__":
    app.run(debug=True)