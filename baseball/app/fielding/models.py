import mysql.connector as dbapi
from flask import current_app as app

class Fielding:
    COLUMNS = {
        'playerID' : 'str',
        'yearID' : 'int',
        'stint' : 'int',
        'teamID' : 'str',
        'lgID' : 'str',
        'pos' : 'str',
        'g' : 'int',
        'gs' : 'int',
        'innOuts' : 'int',
        'po' : 'int',
        'a' : 'int',
        'e' : 'int',
        'dp' : 'int',
    }
    keyvalues = {
        'kplayerID' : '',
        'kyearID' : 0,
        'kstint' : 0,
        'kpos' : ''
    }
    
    def __init__(self):
        self.app = app

    def view_fielding(self, queries, sort_by=None, order=None, exclude_null=True): 
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            select_query = 'SELECT '
            select_query += ", ".join(self.COLUMNS.keys())
            select_query += ' FROM fielding WHERE '

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
            return results
        except dbapi.Error as err:
            db.rollback()
            results = []
            return results
        finally:
            cursor.close()
            db.close()
    
    def update_fielding(self, new_data):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            update_query = 'UPDATE fielding SET '
            print("NEW_DATA", new_data)
            
            new_values = []
            for k, v in new_data.items():
                if '\'' in v:
                    v = v.replace('\'', '\\\'')
                if v == 'None' or v == None:
                    new_values.append("fielding." + k + ' = NULL')
                elif self.COLUMNS[k] == 'int':
                    new_values.append("fielding." + k + ' = ' + v)
                elif self.COLUMNS[k] == 'str':
                    new_values.append("fielding." + k + ' = \'' + v + '\'')
            update_query += ", ".join(new_values)
            update_query += f' WHERE playerID = \'{self.keyvalues["kplayerID"]}\' AND \
                             yearID = {self.keyvalues["kyearID"]} AND stint = {self.keyvalues["kstint"]} AND \
                             pos = \'{self.keyvalues["kpos"]}\';'
            print()
            print(update_query)
            cursor.execute(update_query)
            db.commit()
            cursor.close()
            db.close()
            return True
        except dbapi.Error as err:
            db.rollback()
            cursor.close()
            db.close()
            return False

    def delete_fielding(self):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()

            delete_query = f'DELETE FROM fielding WHERE playerID = \'{self.keyvalues["kplayerID"]}\' AND \
                             yearID = {self.keyvalues["kyearID"]} AND stint = {self.keyvalues["kstint"]} AND \
                             pos = \'{self.keyvalues["kpos"]}\';'
            print()
            print(delete_query)
            cursor.execute(delete_query)
            db.commit()
            cursor.close()
            db.close()
            return True
        except dbapi.Error as err:
            db.rollback()
            cursor.close()
            db.close()
            return False

    def insert_fielding(self, new_data):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            insert_query = 'INSERT INTO fielding ('
            insert_query += ", ".join(self.COLUMNS.keys())
            insert_query += ') VALUES ('
            values = []
            for k,v in self.COLUMNS.items():
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
            cursor.close()
            db.close()
            return True
        except dbapi.Error as err:
            db.rollback()
            cursor.close()
            db.close()
            return False