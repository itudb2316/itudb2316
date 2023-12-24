# app/appearances/__init__.py
from flask import Blueprint

# Create a blueprint instance
appearances_blueprint = Blueprint('appearances', __name__, 
                               template_folder='templates', 
                               static_folder='static', 
                               static_url_path='/appearances/static')

# Import views and models to make them accessible when the blueprint is registered
from . import views, models, search