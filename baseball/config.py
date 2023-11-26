import maskPassword

class Config:
    # Flask app configuration
    DEBUG = True 
    SECRET_KEY = 'hcq94qhf394f0bu80q82093r'

    # MySQL database configuration
    MYSQL_CONN = {
        'host' : 'localhost',
        'user' : 'root',
        'password' : maskPassword.maskPsw(),
        'database' : 'lahman_2014'
    } 

    PER_PAGE = 16