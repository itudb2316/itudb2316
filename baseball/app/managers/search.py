from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators
from wtforms.validators import DataRequired, Length

# This section will be rearranged according to columns of 'managers' table.
class ManagersSearchForm(FlaskForm):
    lahmanID = IntegerField('Lahman ID',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the player\'s Lahman ID'})
    playerID = StringField('Player ID', [Length(max=9)], default="", render_kw={'placeholder': 'Enter the player\'s ID'})
    managerID = StringField('Manager ID', [Length(max=10)], default="", render_kw={'placeholder': 'Enter the manager\'s ID'})
    hofID = StringField('Hall of Fame ID', [Length(max=10)], default="", render_kw={'placeholder': 'Enter the Hall of Fame ID'})
    birthYear = IntegerField('Birth Year',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the player\'s birth year'})
    birthMonth = IntegerField('Birth Month',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the player\'s birth month'})
    birthDay = IntegerField('Birth Day',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the player\'s birth day'})
    birthCountry = StringField('Birth Country', [Length(max=50)], default="", render_kw={'placeholder': 'Enter the player\'s birth country'})
    birthState = StringField('Birth State', [Length(max=2)], default="", render_kw={'placeholder': 'Enter the player\'s birth state'})
    birthCity = StringField('Birth City', [Length(max=50)], default="", render_kw={'placeholder': 'Enter the player\'s birth city'})
    deathYear = IntegerField('Death Year',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the player\'s death year'})
    deathMonth = IntegerField('Death Month',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the player\'s death month'})
    deathDay = IntegerField('Death Day',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the player\'s death day'})
    deathCountry = StringField('Death Country', [Length(max=50)], default="", render_kw={'placeholder': 'Enter the player\'s death country'})
    deathState = StringField('Death State', [Length(max=2)], default="", render_kw={'placeholder': 'Enter the player\'s death state'})
    deathCity = StringField('Death City', [Length(max=50)], default="", render_kw={'placeholder': 'Enter the player\'s death city'})
    nameFirst = StringField('First Name', [Length(max=50)], default="", render_kw={'placeholder': 'Enter the player\'s first name'})
    nameLast = StringField('Last Name', [Length(max=50)], default="", render_kw={'placeholder': 'Enter the player\'s last name'})
    nameNote = StringField('Name Note', [Length(max=255)], default="", render_kw={'placeholder': 'Enter the player\'s name note'})
    nameGiven = StringField('Given Name', [Length(max=255)], default="", render_kw={'placeholder': 'Enter the player\'s given name'})
    nameNick = StringField('Nickname', [Length(max=255)], default="", render_kw={'placeholder': 'Enter the player\'s nickname'})
    weight = IntegerField('Weight',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the player\'s weight'})
    height = IntegerField('Height',validators=[validators.Optional()], default=None, render_kw={'placeholder': 'Enter the player\'s height'})
    bats = StringField('Bats', [Length(max=1)], default="", render_kw={'placeholder': 'Enter the player\'s bats'})
    throws = StringField('Throws', [Length(max=1)], default="", render_kw={'placeholder': 'Enter the player\'s throws'})
    debut = StringField('Debut', [Length(max=10)], default="", render_kw={'placeholder': 'Enter the player\'s debut'})
    finalGame = StringField('Final Game', [Length(max=10)], default="", render_kw={'placeholder': 'Enter the player\'s final game'})
    college = StringField('College', [Length(max=50)], default="", render_kw={'placeholder': 'Enter the player\'s college'})
    lahman40ID = StringField('Lahman 40 ID', [Length(max=9)], default="", render_kw={'placeholder': 'Enter the player\'s Lahman 40 ID'})
    lahman45ID = StringField('Lahman 45 ID', [Length(max=9)], default="", render_kw={'placeholder': 'Enter the player\'s Lahman 45 ID'})
    retroID = StringField('Retro ID', [Length(max=9)], default="", render_kw={'placeholder': 'Enter the player\'s retro ID'})
    holtzID = StringField('Holtz ID', [Length(max=9)], default="", render_kw={'placeholder': 'Enter the player\'s Holtz ID'})
    bbrefID = StringField('Baseball Reference ID', [Length(max=9)], default="", render_kw={'placeholder': 'Enter the player\'s Baseball Reference ID'})
    submit = SubmitField('Search', render_kw={'class': 'btn btn-outline-secondary'})