import mysql.connector as dbapi
from flask import current_app as app
from app.tools import list2dict

class Managers:

    # Column names for Managers table will be inserted here.
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

    def view_managers(self, queries, sort_by=None, order=None, exclude_null=True): 
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            select_query = 'SELECT '
            select_query += ", ".join(self.COLUMNS.keys())
            select_query += ' FROM managers WHERE '
            
            conditions = []
            for k,v in queries.items():
                if v == 'None' or v == None:
                    continue
                if self.COLUMNS[k] == 'int':
                    conditions.append("managers." + k + ' = ' + v)
                elif self.COLUMNS[k] == 'str':
                    conditions.append("managers." + k + ' = \'' + v + '\'')
            select_query += " AND ".join(conditions)
            if len(conditions) == 0:
                select_query = select_query.removesuffix('WHERE ')

            if sort_by != None:
                select_query += ' ORDER BY '
                if exclude_null:
                    select_query += 'CASE WHEN ' + sort_by + ' IS NULL THEN 1 ELSE 0 END, '
                
                select_query += sort_by + ' ' + order
            
            select_query += ';'

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
    
    def update_managers(self, key, new_data):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            update_query = 'UPDATE managers SET '

            print("NEW_DATA", new_data)
            
            new_values = []
            for k,v in new_data.items():
                if '\'' in v:
                    v = v.replace('\'', '\\\'')
                if v == 'None' or v == None:
                    new_values.append("managers." + k + ' = NULL')
                elif self.COLUMNS[k] == 'int':
                    new_values.append("managers." + k + ' = ' + v)
                elif self.COLUMNS[k] == 'str':
                    new_values.append("managers." + k + ' = \'' + v + '\'')
            update_query += ", ".join(new_values)
            update_query += ' WHERE managers.lahmanID = ' + key + ";"


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
        

    def delete_managers(self, key):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()

            delete_query = 'DELETE FROM managers WHERE managers.lahmanID = ' + key + ';'
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

        return results

    def insert_managers(self, new_data):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()

            managers = app.config['PLAYERS']
            
            insert_query = 'INSERT INTO managers ('
            
            insert_query += ", ".join(managers.COLUMNS.keys())
                                #.join([column_name for column_name in managers.COLUMNS.keys()
                                       #if column_name != 'lahmanID']) #primary key

            insert_query += ') VALUES ( '
            
            values = []
            for k,v in managers.COLUMNS.items():
                #if(k == 'lahmanID'): #primary key
                    #continue

                if(k not in new_data.keys()):
                    values.append("NULL")
                    continue
                
                value = new_data[k]
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
