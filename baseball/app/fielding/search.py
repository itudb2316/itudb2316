from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators
from wtforms.validators import DataRequired, Length

class FieldingSearchForm(FlaskForm):
    mksk_playerID = StringField('Player ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the player\'s ID'})
    mksk_yearID = IntegerField('Year', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the year'})
    mksk_stint = IntegerField('Stint', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter player\'s stint'})
    sc_teamID = StringField('Team ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the team ID'})
    sc_lgID = StringField('League ID', [Length(max=100)], default="", render_kw={'placeholder': 'Enter position'})
    mk_pos = StringField('Position', [Length(max=100)], default="", render_kw={'placeholder': 'Enter the player\'s position'})
    mc_g = IntegerField('Games', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games'})
    mc_gs = IntegerField('Games Started', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games started'})
    mc_innOuts = IntegerField('In Outs', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Time played in the field expressed as outs '})
    mc_po = IntegerField('Putouts', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of putouts'})
    mc_a = IntegerField('Assists', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of assists'})
    mc_e = IntegerField('Errors', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of errors'})
    mc_dp = IntegerField('Double Plays', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of double plays'})   
    mc_pb = IntegerField('Passed Balls (by catchers)', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of passed balls'})
    mc_wp = IntegerField('Wild Pitches (by catchers)', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of wild pitches'})
    mc_sb = IntegerField('Opponent Stolen Base (by catchers)', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of opponent stolen base'})
    mc_cs = IntegerField('Opponents Caught Stealing (by catchers)', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of opponents caught stealing'})
    mc_zr = IntegerField('Zone Rating', validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of zone rating'})
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-outline-secondary'})