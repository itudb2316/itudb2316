from flask import render_template
from . import home_blueprint as app

@app.route('/')
@app.route('/home')
@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/error/<string:message>')
def error(message):
    return render_template('error.html', prompt=message)