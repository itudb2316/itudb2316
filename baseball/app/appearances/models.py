import mysql.connector as dbapi
from flask import current_app as app
from app.tools import list2dict

class Appearances:
    
    COLUMNS = {
        "yearID": "int",
        "teamID": "str",
        "lgID": "str",
        "playerID": "str",
        "G_all": "int",
        "G_batting": "int",
        "G_defense": "int",
        "G_p": "int",
        "G_c": "int",
        "G_1b": "int",
        "G_2b": "int",
        "G_3b": "int",
        "G_ss": "int",
        "G_lf": "int",
        "G_cf": "int",
        "G_rf": "int",
        "G_of": "int",
        "G_dh": "int",
        "G_ph": "int",
        "G_pr": "int"
    }

    def __init__(self):
        self.app = app


    def view_appearances(self, queries, sort_by=None, order=None, exclude_null=True): 
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            select_query = 'SELECT '
            select_query += ", ".join(self.COLUMNS.keys())
            select_query += ' FROM appearances WHERE '
            
            conditions = []
            for k,v in queries.items():
                if v == 'None' or v == None:
                    continue
                if self.COLUMNS[k] == 'int':
                    conditions.append("appearances." + k + ' = ' + v)
                elif self.COLUMNS[k] == 'str':
                    conditions.append("appearances." + k + ' = \'' + v + '\'')
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
    
    def update_appearances(self, key1, key2, key3, new_data):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            update_query = 'UPDATE appearances SET '

            print("NEW_DATA", new_data)
            
            new_values = []
            for k,v in new_data.items():
                if '\'' in v:
                    v = v.replace('\'', '\\\'')
                if v == 'None' or v == None:
                    new_values.append("appearances." + k + ' = NULL')
                elif self.COLUMNS[k] == 'int':
                    new_values.append("appearances." + k + ' = ' + v)
                elif self.COLUMNS[k] == 'str':
                    new_values.append("appearances." + k + ' = \'' + v + '\'')
            update_query += ", ".join(new_values)
            update_query += ' WHERE appearances.yearID = ' + key1 + " AND appearances.teamID = \'" + key2 + "\' AND appearances.playerID = \'" + key3 + '\' ;'


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
        

    def delete_appearances(self, key1, key2, key3):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()

            delete_query = 'DELETE FROM appearances WHERE appearances.yearID = ' + key1 + " AND appearances.teamID = \'" + key2 + "\' AND appearances.playerID = \'" + key3 + '\' ;'
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

    def insert_appearances(self, new_data):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()

            appearances = app.config['APPEARANCES']
            
            insert_query = 'INSERT INTO appearances ('
            
            insert_query += ", ".join(appearances.COLUMNS.keys())
                                #.join([column_name for column_name in players.COLUMNS.keys()
                                       #if column_name != 'lahmanID']) #primary key

            insert_query += ') VALUES ( '
            
            values = []
            for k,v in appearances.COLUMNS.items():
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
