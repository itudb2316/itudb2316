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
                    conditions.append(k + ' = ' + v)
                elif self.header_type[k] == 'str':
                    conditions.append(k + ' = \'' + v + '\'')
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
            
    def insert_batting(self, key, data):
        try:
            db = dbapi.connect(**self.app.config['MYSQL_CONN']) 
            cursor = db.cursor()
            insert_query = 'INSERT INTO batting ('
            for key in self.header_type.keys():
                insert_query += key + ', '
            insert_query = insert_query.removesuffix(', ')
            insert_query += ') VALUES ('
            columns = []
            for k,v in data.items():
                if v == 'None' or v == None:
                    columns.append(k + 'NULL')
                if self.header_type[k] == 'int':
                    columns.append(v + ', ')
                elif self.header_type[k] == 'str':
                    columns.append('\'' + v + '\'' + ', ')
            insert_query += ', '.join(columns)
            insert_query = insert_query.removesuffix(', ')
            insert_query += ')'
            print()
            print(insert_query)
            cursor.execute(insert_query)
            result = cursor.fetchall()
            db.commit()
        except dbapi.Error as err:
            db.rollback()
            result = []
        finally:
            cursor.close()
            db.close()
        return result

    def update_batting(self, keys, data):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            update_query = 'UPDATE batting SET '
            conditions = []
            for k,v in data.items():
                if v == 'None' or v == None:
                    conditions.append(k + ' NULL')
                if self.header_type[k] == 'int':
                    conditions.append(k + ' = ' + v)
                elif self.header_type[k] == 'str':
                    conditions.append(k + ' = \'' + v + '\'')
            update_query += ', '.join(conditions)
            update_query += ' WHERE playerID = ' + keys[0] + ' AND yearID = ' + keys[1] + 'AND teamID = ' + keys[2] + 'AND lgID = ' + keys[3]
            print()
            print(update_query)
            cursor.execute(update_query)
            result = cursor.fetchall()
            db.commit()
            return result
        except dbapi.Error as err:
            db.rollback()
        finally:
            cursor.close()
            db.close()
            
    def delete_batting(self, row):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.header)
            delete_query = 'DELETE FROM fielding WHERE '
            for i in range(len(self.header)):
                if data[self.header[i]] == 'None':
                    condition = self.header[i] + ' IS NULL AND '
                elif self.column_types[i] == 'int':
                    condition = self.header[i] + ' = ' + data[self.header[i]] + ' AND '
                elif self.column_types[i] == 'str':
                    condition = self.header[i] + ' = \'' + data[self.header[i]] + '\' AND '
                delete_query += condition
            delete_query = delete_query.removesuffix(' AND ')
            print()
            print(delete_query)
            cursor.execute(delete_query)
            db.commit()
        except dbapi.Error as err:
            db.rollback()
        finally:
            cursor.close()
            db.close()