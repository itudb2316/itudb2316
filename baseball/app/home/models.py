import mysql.connector as dbapi
from flask import current_app as app
import datetime


def getBirthdayPlayers():
    try:
        db =  dbapi.connect(**app.config['MYSQL_CONN'])
        cursor = db.cursor()

        #get today's date
        select_query = 'SELECT players.lahmanID, players.nameFirst, players.nameLast, players.birthYear, players.birthMonth, players.birthDay FROM players WHERE players.birthMonth = ' + str(datetime.datetime.now().month) + ' AND players.birthDay = ' + str(datetime.datetime.now().day) + ';'

        print()
        print(select_query)
        cursor.execute(select_query)
        results = cursor.fetchall()
        db.commit()

    except dbapi.Error as err:
        db.rollback()
        results = []
    finally:
        cursor.close()
        db.close()
    return results