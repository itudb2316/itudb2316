from os import getenv
from dotenv import load_dotenv

class Config:
    # Flask app configuration
    DEBUG = True 
    SECRET_KEY = 'hcq94qhf394f0bu80q82093r'

    load_dotenv() # Load environment variables from .env file
    #.env file is located in root directory of project

    # MySQL database configuration
    MYSQL_CONN = {
        'host' : getenv('DB_HOST', 'localhost'),
        'user' : getenv('DB_USER', 'root'),
        'password' : getenv('DB_PASSWORD'),
        'database' : 'lahman_2014'
    } 
    
    PER_PAGE = 16