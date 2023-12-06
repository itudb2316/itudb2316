import mysql.connector as dbapi
from flask import current_app as app
from app.tools import list2dict

class Fielding:
    HEADER = ['playerID', 'yearID', 'stint', 'teamID', 'lgID', 'pos', 
              'g', 'gs', 'innOuts', 'po', 'a', 'e', 'dp']
    COL_TYPES = ['str', 'int', 'int', 'str', 'str', 'str', 'int', 
                 'int', 'int', 'int', 'int', 'int', 'int']
    
    def __init__(self):
        self.app = app

    def view_fielding(self, row, sort_by=None, order=None, exclude_null=True): 
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.HEADER)
            select_query = 'SELECT '
            select_query += ", ".join(self.HEADER)
            select_query += ' FROM fielding WHERE '

            for i in range(len(self.HEADER)):
                if data[self.HEADER[i]] == 'None':
                    continue
                if self.COL_TYPES[i] == 'int':
                    condition = self.HEADER[i] + ' = ' + data[self.HEADER[i]] + ' AND '
                elif self.COL_TYPES[i] == 'str':
                    condition = self.HEADER[i] + ' = \'' + data[self.HEADER[i]] + '\' AND '
                select_query += condition
            if select_query[-6:-1] == 'WHERE':
                select_query = select_query.removesuffix(' WHERE ')
            else:
                select_query = select_query.removesuffix(' AND ')

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
    
    def update_fielding(self, transmit, row):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.HEADER)
            update_query = 'UPDATE fielding SET '
            for i in range(len(self.HEADER)):
                if data[self.HEADER[i]] == 'None':
                    update_query += self.HEADER[i] + ' = NULL AND '
                elif self.COL_TYPES[i] == 'int':
                    update_query += self.HEADER[i] + ' = ' + data[self.HEADER[i]] + ' , '
                elif self.COL_TYPES[i] == 'str':
                    update_query += self.HEADER[i] + ' = \'' + data[self.HEADER[i]] + '\' , '
            update_query = update_query.removesuffix(' , ')
            update_query += ' WHERE '
            for i in range(len(self.HEADER)):
                if transmit[i] == 'None':
                    update_query += self.HEADER[i] + ' IS NULL AND '
                elif self.COL_TYPES[i] == 'int':
                    update_query += self.HEADER[i] + ' = ' + transmit[i] + ' AND '
                elif self.COL_TYPES[i] == 'str':
                    update_query += self.HEADER[i] + ' = \'' + transmit[i] + '\' AND '
            update_query = update_query.removesuffix(' AND ')
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

    def delete_fielding(self, row):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.HEADER)
            delete_query = 'DELETE FROM fielding WHERE '
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
            cursor.close()
            db.close()
            return True
        except dbapi.Error as err:
            db.rollback()
            cursor.close()
            db.close()
            return False

    def insert_fielding(self, row):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.HEADER)
            insert_query = 'INSERT INTO fielding ('
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
            cursor.close()
            db.close()
            return True
        except dbapi.Error as err:
            db.rollback()
            cursor.close()
            db.close()
            return False

"""
class Demo:
    def __init__(self, row):
        self.data = list2dict(row, self.HEADER)

    def insert_fielding(self):
        insert_query = 'INSERT INTO fielding ('
        for i in self.HEADER:
            insert_query += i + ', '
        insert_query = insert_query.removesuffix(', ')
        insert_query += ') VALUES ('
        for i in range(len(self.HEADER)):
            if self.data[self.HEADER[i]] == 'None':
                insert_query += 'NULL, '
            elif self.COL_TYPES[i] == 'int':
                insert_query +=  self.data[self.HEADER[i]] + ', '
            elif self.COL_TYPES[i] == 'str':
                insert_query += '\'' + self.data[self.HEADER[i]] + '\', '
        insert_query = insert_query.removesuffix(', ')
        insert_query += ')'
        print()
        print(insert_query)
"""