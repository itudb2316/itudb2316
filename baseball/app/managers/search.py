from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, SubmitField
from wtforms.validators import DataRequired, Length

# This section is rearranged according to columns of 'managers' table.
class ManagersSearchForm(FlaskForm):
    managerID = StringField('Manager ID', [Length(max=10)], default="", render_kw={'placeholder': 'Enter the manager\'s ID'})
    yearID = IntegerField('Year ID',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the year ID'})
    teamID = StringField('Team ID', [Length(max=3)], default="", render_kw={'placeholder': 'Enter the team ID'})
    lgID = StringField('League ID', [Length(max=2)], default="", render_kw={'placeholder': 'Enter the league ID'})
    inseason = IntegerField('Inseason',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the inseason value'})
    G = IntegerField('Games',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games'})
    W = IntegerField('Wins',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of wins'})
    L = IntegerField('Losses',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of losses'})
    rank_ = IntegerField('Rank',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the rank'})
    plyrMgr = StringField('Player Manager', [Length(max=1)], default="", render_kw={'placeholder': 'Enter the player/manager status'})
    submit = SubmitField('Search', render_kw={'class': 'btn btn-outline-secondary'})

class ManagersInsertForm(FlaskForm):
    managerID = StringField('Manager ID', [Length(max=10), validators.InputRequired()], default="", render_kw={'placeholder': 'Enter the manager\'s ID (REQUIRED)'})
    yearID = IntegerField('Year ID',validators=[validators.InputRequired()], default=None, render_kw={'placeholder': 'Enter the year ID (REQUIRED)'})
    teamID = StringField('Team ID', [Length(max=3), validators.InputRequired()], default="", render_kw={'placeholder': 'Enter the team ID (REQUIRED)'})
    lgID = StringField('League ID', [Length(max=2)], default="", render_kw={'placeholder': 'Enter the league ID'})
    inseason = IntegerField('Inseason',validators=[validators.InputRequired()], default=None, render_kw={'placeholder': 'Enter the inseason value (REQUIRED)'})
    G = IntegerField('Games',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of games'})
    W = IntegerField('Wins',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of wins'})
    L = IntegerField('Losses',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the number of losses'})
    rank_ = IntegerField('Rank',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the rank'})
    plyrMgr = StringField('Player Manager', [Length(max=1)], default="", render_kw={'placeholder': 'Enter the player/manager status'})
    submit = SubmitField('Insert', render_kw={'class': 'btn btn-outline-secondary'})