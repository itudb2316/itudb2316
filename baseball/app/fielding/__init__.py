# app/fielding/__init__.py
from flask import Blueprint

# Create a blueprint instance
fielding_blueprint = Blueprint('fielding', __name__, 
                               template_folder='templates', 
                               static_folder='static', 
                               static_url_path='/fielding/static')

# Import views and models to make them accessible when the blueprint is registered
from . import views, models, search