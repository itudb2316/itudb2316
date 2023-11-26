from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class FieldingSearchForm(FlaskForm):
    playerID = StringField('Player ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the player\'s ID'})
    year = IntegerField('Year', default=-1, render_kw={'placeholder': 'Enter the year'})
    stint = IntegerField('Stint', default=-1, render_kw={'placeholder': 'Enter player\'s stint'})
    teamID = StringField('Team ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the team ID'})
    lgID = StringField('League ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter position'})
    pos = StringField('Position', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the player\'s position'})
    games = IntegerField('Games', default=-1, render_kw={'placeholder': 'Enter the number of games'})
    gs = IntegerField('Games Started', default=-1, render_kw={'placeholder': 'Enter the number of games started'})
    innOuts = IntegerField('In Outs', default=-1, render_kw={'placeholder': 'Time played in the field expressed as outs '})
    po = IntegerField('Putouts', default=-1, render_kw={'placeholder': 'Enter the number of putouts'})
    a = IntegerField('Assists', default=-1, render_kw={'placeholder': 'Enter the number of assists'})
    e = IntegerField('Errors', default=-1, render_kw={'placeholder': 'Enter the number of errors'})
    dp = IntegerField('Double Plays', default=-1, render_kw={'placeholder': 'Enter the number of double plays'})
    submit = SubmitField('Search', render_kw={'class': 'btn btn-outline-secondary'})