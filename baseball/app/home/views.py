from flask import render_template
from . import home_blueprint as app
from .models import getBirthdayPlayers
import datetime

@app.route('/')
@app.route('/home')
@app.route('/home/')
def home():
    bday_players = getBirthdayPlayers()

    return render_template('home.html', bday_players=bday_players)

@app.route('/error/<string:message>')
def error(message):
    return render_template('error.html', prompt=message)