from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators
from wtforms.validators import DataRequired, Length

class AppearancesSearchForm(FlaskForm):
    yearID = IntegerField('Year',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the year'})
    teamID = StringField('Team ID', [Length(max=3)], default="", render_kw={'placeholder': 'Enter the team\'s ID'})
    lgID = StringField('League ID', [Length(max=2)], default="", render_kw={'placeholder': 'Enter the league\'s ID'})
    playerID = StringField('Player ID', [Length(max=9)], default="", render_kw={'placeholder': 'Enter the player\'s ID'})
    G_all = IntegerField('Games',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games'})
    G_batting = IntegerField('Games in which player batted',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as batter'})
    G_defense = IntegerField('Games in which player appeared on defense',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as defense'})
    G_p = IntegerField('Games as Pitcher',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as pitcher'})
    G_c = IntegerField('Games as Catcher',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as catcher'})
    G_1b = IntegerField('Games as First Base',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as first base'})
    G_2b = IntegerField('Games as Second Base',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as second base'})
    G_3b = IntegerField('Games as Third Base',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as third base'})
    G_ss = IntegerField('Games as Shortstop',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as shortstop'})
    G_lf = IntegerField('Games as Left Field',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as left field'})
    G_cf = IntegerField('Games as Center Field',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as center field'})
    G_rf = IntegerField('Games as Right Field',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as right field'})
    G_of = IntegerField('Games as Outfield',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as outfield'})
    G_dh = IntegerField('Games as Designated Hitter',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as designated hitter'})
    G_ph = IntegerField('Games as Pinch Hitter',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as pinch hitter'})
    G_pr = IntegerField('Games as Pinch Runner',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games as pinch runner'})

    submit = SubmitField('Search', render_kw={'class': 'btn btn-outline-secondary'})
