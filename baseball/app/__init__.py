from flask import Flask
from config import Config
from flask_wtf import CSRFProtect
from .tools import RowListConverter
# Import tables
from app.fielding.models import Fielding
    
def create_app():
    app = Flask(__name__)
    csrf = CSRFProtect(app)

    app.url_map.converters.update({'row_list' : RowListConverter})

    # Load configuration from the Config class
    app.config.from_object(Config)
    # Configure tables
    app.config['FIELDING'] = Fielding()

    # Register blueprints
    from app.home import home_blueprint
    from app.fielding import fielding_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(fielding_blueprint)

    return app