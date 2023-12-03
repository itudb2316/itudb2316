from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class TeamshalfSearchForm(FlaskForm):
    name = StringField('Team Name', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the team\'s name'})
    yearID = IntegerField('Year', default=-1, render_kw={'placeholder': 'Enter the year'})
    teamID = StringField('Team ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the team\'s ID'})
    lgID = StringField('League ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the team\'s league ID'})
    divID = StringField('Division ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the team\'s division ID'})
    Half = StringField('Half', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the half season'})
    DivWin = StringField('Division Win', [Length(max=100)], default="", render_kw={'placeholder': 'Has the team won the division? (Y for yes, N for no)'})
    Rank = StringField('Ranking', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the team\'s ranking'})
    G = IntegerField('Games Played', default=-1, render_kw={'placeholder': 'Enter the amount of games that the team has played'})
    W = IntegerField('Wins', default=-1, render_kw={'placeholder': 'Enter the amount of wins that the team has'})
    L = IntegerField('Losses', default=-1, render_kw={'placeholder': 'Enter the amount of losses that the team has'})
    submit = SubmitField('Search', render_kw={'class': 'btn btn-outline-secondary'})