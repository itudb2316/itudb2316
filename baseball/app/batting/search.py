from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class BattingSearchForm(FlaskForm):
    playerID = StringField('Player ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the player\'s ID'})
    year = IntegerField('Year', default=-1, render_kw={'placeholder': 'Enter the year'})
    stint = IntegerField('Stint', default=-1, render_kw={'placeholder': 'Enter the player\'s stint'})
    teamID = StringField('Team', [Length(max=3)], default="", render_kw={'placeholder': 'Enter the player\'s team'})
    lgID = StringField('League', [Length(max=2)], default="", render_kw={'placeholder': 'Enter the player\'s league in MLB'})
    G = IntegerField('Games', default=-1, render_kw={'placeholder': 'Enter the number of games'})
    AB = IntegerField('At bats', default=-1, render_kw={'placeholder': 'Enter the number of times the player was a batter'})
    R = IntegerField('Runs', default=-1, render_kw={'placeholder': 'Enter the number of runs the player has'})
    H = IntegerField('Hits', default=-1, render_kw={'placeholder': 'Enter the number of hits the player has'})
    X2B = IntegerField('Doubles', default=-1, render_kw={'placeholder': 'Enter the number of doubles the player has'})
    X3B = IntegerField('Triples', default=-1, render_kw={'placeholder': 'Enter the number of triples the player has'})
    HR = IntegerField('Home runs', default=-1, render_kw={'placeholder': 'Enter the number of home runs the player has'})
    RBI = IntegerField('Runs batted in', default=-1, render_kw={'placeholder': 'Enter the number of runs from the player\'s hit'})
    SB = IntegerField('Stolen bases', default=-1, render_kw={'placeholder': 'Enter the number of bases the player stole'})
    CS = IntegerField('Caught stealing', default=-1, render_kw={'placeholder': 'Enter the number of times the player was caught stealing a base'})
    SO = IntegerField('Strikeouts', default=-1, render_kw={'placeholder': 'Enter the number of times the player was out'})
    submit = SubmitField('Search', render_kw={'class': 'btn btn-outline-secondary'})