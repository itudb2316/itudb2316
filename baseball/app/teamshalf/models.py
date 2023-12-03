import mysql.connector as dbapi
from flask import current_app as app
from app.tools import list2dict

class Teamshalf:
    HEADER = ['yearID', 'teamID', 'Half', 'DivWin', 'Rank', 'G AS Games Played',
              'W AS Wins', 'L AS Losses']
    COL_TYPES = ['int', 'str', 'str', 'str', 'int', 'int', 'int', 'int']

    def __init__(self):
        self.app = app

    def view_teams(self, row): 
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            headers = ['name AS Team Name', 'yearID AS Year', 'teamID AS Team ID', 'lgID AS League ID', 'divID AS Division ID', 'Half', 'DivWin AS Division Win', 'Rank AS Ranking', 'G AS Games Played',
              'W AS Wins', 'L AS Losses']
            column_types = ['str', 'int', 'str', 'str', 'str', 'str', 'str', 'int', 'int', 'int', 'int']
            data = list2dict(row, headers)
            select_query = 'SELECT '
            for col in headers:
                select_query += col + ', '
            select_query = select_query.removesuffix(', ')
            select_query += ' FROM teamshalf JOIN teams ON teamID WHERE '
            for i in range(len(headers)):
                if data[headers[i]] == 'None':
                    continue
                if column_types[i] == 'int':
                    condition = headers[i] + ' = ' + data[headers[i]] + ' AND '
                elif column_types[i] == 'str':
                    condition = headers[i] + ' = \'' + data[headers[i]] + '\' AND '
                select_query += condition
            if select_query[-6:-1] == 'WHERE':
                select_query = select_query.removesuffix(' WHERE ')
            else:
                select_query = select_query.removesuffix(' AND ')
            print()
            print(select_query)
            cursor.execute(select_query)
            results = cursor.fetchall()
            db.commit()

        except dbapi.Error as err:
            db.rollback()
        finally:
            cursor.close()
            db.close()
        return results

    def update_teams(self, transmit, row):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.HEADER)
            update_query = 'UPDATE teamshalf SET '
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
        except dbapi.Error as err:
            db.rollback()
        finally:
            cursor.close()
            db.close()

    def delete_teams(self, row):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.HEADER)
            delete_query = 'DELETE FROM teamshalf WHERE '
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

    def insert_teams(self, row):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.HEADER)
            insert_query = 'INSERT INTO teamshalf ('
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