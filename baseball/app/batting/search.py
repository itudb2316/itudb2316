from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators
from wtforms.validators import DataRequired, Length

class BattingSearchForm(FlaskForm):
    mksk_playerID = StringField('Player ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the player\'s ID'})
    mksk_yearID = IntegerField('Year', validators=[validators.Optional(), validators.NumberRange(min=1871)], default=None, render_kw={'placeholder': 'Enter the year'})
    mksk_stint = IntegerField('Stint', validators=[validators.Optional(), validators.NumberRange(min=1)], default=None, render_kw={'placeholder': 'Enter the player\'s stint'})
    sc_teamID = StringField('Team', [Length(max=3)], default="", render_kw={'placeholder': 'Enter the player\'s team'})
    sc_lgID = StringField('League', [Length(max=2)], default="", render_kw={'placeholder': 'Enter the player\'s league in MLB'})
    mc_G = IntegerField('Games', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games'})
    mc_AB = IntegerField('At bats', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of times the player was a batter'})
    mc_R = IntegerField('Runs', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of runs the player has'})
    mc_H = IntegerField('Hits', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of hits the player has'})
    mc_X2B = IntegerField('Doubles', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of doubles the player has'})
    mc_X3B = IntegerField('Triples', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of triples the player has'})
    mc_HR = IntegerField('Home runs', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of home runs the player has'})
    mc_RBI = IntegerField('Runs batted in', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of runs from the player\'s hit'})
    mc_SB = IntegerField('Stolen bases', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of bases the player stole'})
    mc_CS = IntegerField('Caught stealing', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of times the player was caught stealing a base'})
    mc_BB = IntegerField('Base on balls', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the base on balls of the player'})
    mc_SO = IntegerField('Strikeouts', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of times the player was out'})
    mc_IBB = IntegerField('Intentional walks', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of intentional walks by the player'})
    mc_HBP = IntegerField('Hits by pitch', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of times the player was hit by pitch'})
    mc_SH = IntegerField('Sacrifice hits', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the sacrifice hits of the player'})
    mc_SF = IntegerField('Sacrifice flies', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the sacrifice flies of the player'})
    mc_GIDP = IntegerField('Plays grounded into double play', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the hits grounded into double plays by the player'})        
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-outline-secondary'})