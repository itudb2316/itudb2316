from flask import render_template
from . import home_blueprint as app

@app.route('/')
@app.route('/home')
@app.route('/home/')
def home():
    return render_template('home.html')