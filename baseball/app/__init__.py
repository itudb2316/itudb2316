from flask import Flask
from config import Config
from flask_wtf import CSRFProtect
from .tools import RowListConverter
# Import tables
from app.fielding.models import Fielding
from app.players.models import Players
from app.batting.models import Batting
from app.managers.models import Managers
from app.teamshalf.models import Teamshalf
from app.teams.models import Teams
    
def create_app():
    app = Flask(__name__)
    csrf = CSRFProtect(app)

    app.url_map.converters.update({'row_list' : RowListConverter})

    # Load configuration from the Config class
    app.config.from_object(Config)
    # Configure tables
    app.config['FIELDING'] = Fielding()
    app.config['PLAYERS'] = Players()
    app.config['MANAGERS'] = Managers()
    app.config['BATTING'] = Batting()
    app.config['TEAMSHALF'] = Teamshalf()
    app.config['TEAMS'] = Teams()

    # Register blueprints
    from app.home import home_blueprint
    from app.fielding import fielding_blueprint
    from app.players import players_blueprint
    from app.managers import managers_blueprint
    from app.batting import batting_blueprint
    from app.teamshalf import teamshalf_blueprint
    from app.teams import teams_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(fielding_blueprint)
    app.register_blueprint(players_blueprint)
    app.register_blueprint(managers_blueprint)
    app.register_blueprint(batting_blueprint)
    app.register_blueprint(teamshalf_blueprint)
    app.register_blueprint(teams_blueprint)

    return app