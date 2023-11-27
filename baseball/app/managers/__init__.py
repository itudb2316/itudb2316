# app/managers/__init__.py
from flask import Blueprint

# Create a blueprint instance
managers_blueprint = Blueprint('managers', __name__, 
                               template_folder='templates', 
                               static_folder='static', 
                               static_url_path='/managers/static')

# Import views and models to make them accessible when the blueprint is registered
from . import views, models, search