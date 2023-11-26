from flask import Flask
from config import Config
from flask_wtf import CSRFProtect
from .tools import RowListConverter
# Import tables
from app.fielding.models import Fielding
from app.players.models import Players    
    
def create_app():
    app = Flask(__name__)
    csrf = CSRFProtect(app)

    app.url_map.converters.update({'row_list' : RowListConverter})

    # Load configuration from the Config class
    app.config.from_object(Config)
    # Configure tables
    app.config['FIELDING'] = Fielding()
    app.config['PLAYERS'] = Players()

    # Register blueprints
    from app.home import home_blueprint
    from app.fielding import fielding_blueprint
    from app.players import players_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(fielding_blueprint)
    app.register_blueprint(players_blueprint)

    return app