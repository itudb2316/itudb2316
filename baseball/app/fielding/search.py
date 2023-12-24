from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators
from wtforms.validators import DataRequired, Length

class FieldingSearchForm(FlaskForm):
    playerID = StringField('Player ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the player\'s ID'})
    yearID = IntegerField('Year', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the year'})
    stint = IntegerField('Stint', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter player\'s stint'})
    teamID = StringField('Team ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the team ID'})
    lgID = StringField('League ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter position'})
    pos = StringField('Position', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the player\'s position'})
    g = IntegerField('Games', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games'})
    gs = IntegerField('Games Started', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games started'})
    innOuts = IntegerField('In Outs', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Time played in the field expressed as outs '})
    po = IntegerField('Putouts', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of putouts'})
    a = IntegerField('Assists', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of assists'})
    e = IntegerField('Errors', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of errors'})
    dp = IntegerField('Double Plays', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of double plays'})   
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-outline-secondary'})