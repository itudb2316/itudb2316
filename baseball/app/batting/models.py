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
            db = dbapi.connect(**self.app.config['MYSQL_CONN']) #**self.app.config['MYSQL_CONN']
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
            
    def insert_batting(self, row):
        try:
            db = dbapi.connect(**self.app.config['MYSQL_CONN']) 
            cursor = db.cursor()
            data = list2dict(row, self.header)
            insert_query = 'INSERT INTO batting ('
            for column in self.header:
                insert_query += column + ', '
            insert_query = insert_query.removesuffix(', ')
            insert_query += ') VALUES ('
            for i in range(len(self.header)):
                if data[self.header[i]] == 'None':
                    insert_query += 'NULL'
                if self.column_types[i] == 'int':
                    insert_query += data[self.header[i]] + ', '
                elif self.column_types[i] == 'str':
                    insert_query += '\'' + data[self.header[i]] + '\', '
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

    def update_batting(self, transmit, row):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.header)
            update_query = 'UPDATE batting SET '
            for i in range(len(self.header)):
                if data[self.header[i]] == 'None':
                    update_query += self.header[i] + ' = NULL AND '
                elif self.column_types[i] == 'int':
                    update_query += self.header[i] + ' = ' + data[self.header[i]] + ' , '
                elif self.column_types[i] == 'str':
                    update_query += self.header[i] + ' = \'' + data[self.header[i]] + '\' , '
            update_query = update_query.removesuffix(' , ')
            update_query += ' WHERE '
            for i in range(len(self.header)):
                if transmit[i] == 'None':
                    update_query += self.header[i] + ' IS NULL AND '
                elif self.column_types[i] == 'int':
                    update_query += self.header[i] + ' = ' + transmit[i] + ' AND '
                elif self.column_types[i] == 'str':
                    update_query += self.header[i] + ' = \'' + transmit[i] + '\' AND '
            update_query = update_query.removesuffix(' AND ')
            print()
            print(update_query)
            cursor.execute(update_query)
            db.commit()
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