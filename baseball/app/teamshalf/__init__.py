# app/players/__init__.py
from flask import Blueprint

# Create a blueprint instance
teamshalf_blueprint = Blueprint('teamshalf', __name__, 
                               template_folder='templates', 
                               static_folder='static', 
                               static_url_path='/teamshalf/static')

# Import views and models to make them accessible when the blueprint is registered
from . import views, models, search