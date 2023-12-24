import mysql.connector as dbapi
from flask import current_app as app
from app.tools import list2dict

class Batting:
    
    header_type = {
        
        'playerID': 'str',
        'yearID': 'int',
        'stint': 'int',
        'teamID': 'str',
        'lgID': 'str',
        'G': 'int',
        'AB': 'int',
        'R': 'int',
        'H': 'int',
        '2B': 'int',
        '3B': 'int',
        'HR': 'int',
        'RBI': 'int',
        'SB': 'int',
        'CS': 'int',
        'SO': 'int'
        
    }
    
    header = ['playerID', 'yearID', 'stint', 'teamID', 'lgID', 'G', 'AB', 'R',
              'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'SO']
    column_types = ['str', 'int', 'int', 'str', 'str', 'int', 'int', 'int',
                    'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int']
    
    def __init__(self):
        self.app = app
        
    def view_batting(self, queries, sort_by=None, order=None, exclude_null=True):
        try:
            db = dbapi.connect(**self.app.config['MYSQL_CONN']) #**self.app.config['MYSQL_CONN']
            cursor = db.cursor()
            select_query = 'SELECT '
            select_query += ", ".join(self.header_type.keys())
            select_query += ' FROM batting WHERE '
            conditions = []
            for k,v in queries.items():
                if v == 'None' or v == None:
                    continue
                if self.header_type[k] == 'int':
                    conditions.append("batting." + k + ' = ' + v)
                elif self.header_type[k] == 'str':
                    conditions.append("batting." + k + ' = \'' + v + '\'')
            select_query += " AND ".join(conditions)
            if len(conditions) == 0:
                select_query = select_query.removesuffix('WHERE ')
            if sort_by != None:
                select_query += ' ORDER BY '
                if exclude_null:
                    select_query += 'CASE WHEN ' + sort_by + ' IS NULL THEN 1 ELSE 0 END, '
                select_query += sort_by + ' ' + order
            print()
            print(select_query)
            cursor.execute(select_query)
            result = cursor.fetchall()
            db.commit()
        except dbapi.Error as err:
            db.rollback()
            result = []
        finally:
            cursor.close()
            db.close()
        return result
            
    def insert_batting(self, data):
        try:
            db = dbapi.connect(**self.app.config['MYSQL_CONN']) 
            cursor = db.cursor()
            battings = app.config['BATTING']
            insert_query = 'INSERT INTO batting ('
            insert_query += ", ".join(battings.header_type.keys())
            insert_query += ') VALUES ( '
            
            values = []
            for k,v in battings.header_type.items():

                if(k not in data.keys()):
                    values.append("NULL")
                    continue
                
                value = data[k]
                if value == 'None' or value == None or value == '':
                    values.append("NULL")
                    continue

                if '\'' in value:
                    value = value.replace('\'', '\\\'')
                
                if v == 'int':
                    values.append(value)
                elif v == 'str':
                    values.append('\'' + value + '\'')

            insert_query += ", ".join(values)
            insert_query += ');'
            print()
            print(insert_query)
            cursor.execute(insert_query)
            db.commit()
        except dbapi.Error as err:
            db.rollback()
        finally:
            cursor.close()
            db.close()

    def update_batting(self, keys, data):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            update_query = 'UPDATE batting SET '
            conditions = []
            for k,v in data.items():
                if v == 'None' or v == None:
                    conditions.append("batting." + k + '= NULL')
                if self.header_type[k] == 'int':
                    conditions.append("batting." + k + ' = ' + v)
                elif self.header_type[k] == 'str':
                    conditions.append("batting." + k + ' = \'' + v + '\'')
            update_query += ', '.join(conditions)
            update_query += ' WHERE playerID = \'' + keys[0] + '\' AND yearID = ' + keys[1] + ' AND stint = ' + keys[2]
            print()
            print(update_query)
            cursor.execute(update_query)
            result = cursor.fetchall()
            db.commit()
        except dbapi.Error as err:
            db.rollback()
            result = []
        finally:
            cursor.close()
            db.close()
        return result
            
    def delete_batting(self, keys):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            delete_query = 'DELETE FROM batting WHERE playerID = \'' + keys[0] + '\' AND yearID = ' + keys[1] + ' AND stint = ' + keys[2]
            print()
            print(delete_query)
            cursor.execute(delete_query)
            results = cursor.fetchall()
            db.commit()
        except dbapi.Error as err:
            db.rollback()
            results = []
        finally:
            cursor.close()
            db.close()