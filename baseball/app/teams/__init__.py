# app/players/__init__.py
from flask import Blueprint

# Create a blueprint instance
teams_blueprint = Blueprint('teams', __name__, 
                               template_folder='templates', 
                               static_folder='static', 
                               static_url_path='/teams/static')

# Import views and models to make them accessible when the blueprint is registered
from . import views, models, search