import mysql.connector as dbapi
from flask import current_app as app
from app.tools import list2dict

class Batting:
    header = ['playerID', 'yearID', 'stint', 'teamID', 'lgID', 'G', 'AB', 'R',
              'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'SO']
    column_types = ['str', 'int', 'int', 'str', 'str', 'int', 'int', 'int',
                    'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int']
    
    def __init__(self):
        self.app = app
        
    def view_batting(self, row):
        try:
            db = dbapi.connect(host="localhost", user="root", password="Herobrine54", database="lahman_2014") #**self.app.config['MYSQL_CONN']
            cursor = db.cursor()
            data = list2dict(row, self.header)
            select_query = 'SELECT '
            for column in self.header:
                select_query += column + ', '
            select_query = select_query.removesuffix(', ')
            select_query += ' FROM batting WHERE '
            for i in range(len(self.header)):
                if data[self.header[i]] == 'None':
                    continue
                if self.column_types[i] == 'int':
                    condition = self.header[i] + ' = ' + data[self.header[i]] + ' AND '
                elif self.column_types[i] == 'str':
                    condition = self.header[i] + ' = \'' + data[self.header[i]] + '\' AND '
                select_query += condition
            if select_query[-6:-1] == 'WHERE':
                select_query = select_query.removesuffix(' WHERE ')
            else:
                select_query = select_query.removesuffix(' AND ')
            print()
            print(select_query)
            cursor.execute(select_query)
            result = cursor.fetchall()
            db.commit()
            return result
        except dbapi.Error as err:
            db.rollback()
        finally:
            cursor.close()
            db.close()