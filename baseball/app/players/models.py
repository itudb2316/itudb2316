import mysql.connector as dbapi
from flask import current_app as app
from app.tools import list2dict

class Players:
    
    COLUMNS = {
    'lahmanID': 'int',
    'playerID': 'str',
    'managerID': 'str',
    'hofID': 'str',
    'birthYear': 'int',
    'birthMonth': 'int',
    'birthDay': 'int',
    'birthCountry': 'str',
    'birthState': 'str',
    'birthCity': 'str',
    'deathYear': 'int',
    'deathMonth': 'int',
    'deathDay': 'int',
    'deathCountry': 'str',
    'deathState': 'str',
    'deathCity': 'str',
    'nameFirst': 'str',
    'nameLast': 'str',
    'nameNote': 'str',
    'nameGiven': 'str',
    'nameNick': 'str',
    'weight': 'int',
    'height': 'int',
    'bats': 'str',
    'throws': 'str',
    'debut': 'str',
    'finalGame': 'str',
    'college': 'str',
    'lahman40ID': 'str',
    'lahman45ID': 'str',
    'retroID': 'str',
    'holtzID': 'str',
    'bbrefID': 'str'
}
    def __init__(self):
        self.app = app

    def view_players(self, queries, sort_by=None, order=None, exclude_null=True): 
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            select_query = 'SELECT '
            select_query += ", ".join(self.COLUMNS.keys())
            select_query += ' FROM players WHERE '
            
            conditions = []
            for k,v in queries.items():
                if v == 'None' or v == None:
                    continue
                if self.COLUMNS[k] == 'int':
                    conditions.append(k + ' = ' + v)
                elif self.COLUMNS[k] == 'str':
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
            results = cursor.fetchall()
            db.commit()
            
        except dbapi.Error as err:
            db.rollback()
            results = []
        finally:
            cursor.close()
            db.close()
        return results
    
    def update_players(self, key, new_data):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            update_query = 'UPDATE players SET '
            
            new_values = []
            for k,v in new_data.items():
                if v == 'None' or v == None:
                    new_values.append(k + ' = NULL')
                elif self.COLUMNS[k] == 'int':
                    new_values.append(k + ' = ' + v)
                elif self.COLUMNS[k] == 'str':
                    new_values.append(k + ' = \'' + v + '\'')
            update_query += ", ".join(new_values)
            update_query += ' WHERE lahmanID = ' + key


            print()
            print(update_query)
            cursor.execute(update_query)
            results = cursor.fetchall()
            db.commit()
            
        except dbapi.Error as err:
            db.rollback()
            results = []
        finally:
            cursor.close()
            db.close()
        return results
        

    def delete_players(self, row):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.HEADER)
            delete_query = 'DELETE FROM players WHERE '
            for i in range(len(self.HEADER)):
                if data[self.HEADER[i]] == 'None':
                    condition = self.HEADER[i] + ' IS NULL AND '
                elif self.COL_TYPES[i] == 'int':
                    condition = self.HEADER[i] + ' = ' + data[self.HEADER[i]] + ' AND '
                elif self.COL_TYPES[i] == 'str':
                    condition = self.HEADER[i] + ' = \'' + data[self.HEADER[i]] + '\' AND '
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

    def insert_players(self, row):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.HEADER)
            insert_query = 'INSERT INTO players ('
            for i in self.HEADER:
                insert_query += i + ', '
            insert_query = insert_query.removesuffix(', ')
            insert_query += ') VALUES ('
            for i in range(len(self.HEADER)):
                if data[self.HEADER[i]] == 'None':
                    insert_query += 'NULL'
                elif self.COL_TYPES[i] == 'int':
                    insert_query +=  data[self.HEADER[i]] + ', '
                elif self.COL_TYPES[i] == 'str':
                    insert_query += '\'' + data[self.HEADER[i]] + '\', '
            insert_query = insert_query.removesuffix(', ')
            insert_query += ')'
            print()
            print(insert_query)
            cursor.execute(insert_query)
            db.commit()
        except dbapi.Error as err:
            db.rollback()
        finally:
            cursor.close()
            db.close()
