import mysql.connector as dbapi
from flask import current_app as app
from app.tools import list2dict

class Teamshalf:
    HEADER = ['yearID', 'teamID', 'Half', 'DivWin', 'teamshalf.Rank', 'G',
              'W', 'L']
    COL_TYPES = ['int', 'str', 'str', 'str', 'int', 'int', 'int', 'int']

    joined_search_headers = ['teamshalf_teams.name', 'teamshalf.yearID', 'teamshalf.teamID', 'teamshalf_teams.lgID', 'teamshalf_teams.divID', 'teamshalf.Half', 'teamshalf.DivWin', 'teamshalf.Rank', 'teamshalf.G',
              'teamshalf.W', 'teamshalf.L']
    joined_search_column_types = ['str', 'int', 'str', 'str', 'str', 'str', 'str', 'int', 'int', 'int', 'int']


    teams_table_insertion_headers = ['name', 'yearID', 'teamID', 'lgID', 'divID', 'teamshalf.Half', 'DivWin', 'teams.Rank', 'G',
              'W', 'L']
    
    teams_table_insertion_column_types = ['str', 'int', 'str', 'str', 'str', 'str', 'str', 'int', 'int', 'int', 'int']


    def __init__(self):
        self.app = app

    def view_teams(self, row): 
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            data = list2dict(row, self.joined_search_headers)
            select_query = 'SELECT DISTINCT '
            for col in self.joined_search_headers:
                select_query += col + ', '
            select_query = select_query.removesuffix(', ')
            select_query += ' FROM teamshalf, teamshalf_teams WHERE teamshalf.teamID=teamshalf_teams.teamID AND '
            for i in range(len(self.joined_search_headers)):
                if data[self.joined_search_headers[i]] == 'None':
                    continue
                if self.joined_search_column_types[i] == 'int':
                    condition = self.joined_search_headers[i] + ' = ' + data[self.joined_search_headers[i]] + ' AND '
                elif self.joined_search_column_types[i] == 'str':
                    condition = self.joined_search_headers[i] + ' = \'' + data[self.joined_search_headers[i]] + '\' AND '
                select_query += condition
            if select_query[-6:-1] == 'WHERE':
                select_query = select_query.removesuffix(' WHERE ')
            else:
                select_query = select_query.removesuffix(' AND ')
            select_query += ';'
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
            new_teamID = ''
            apostrophe = "'"
            new_teamID += apostrophe
            new_teamID += data[self.HEADER[1]]
            new_teamID += apostrophe
            

            teams_table_update_query = 'UPDATE teams SET teamID = '
            teams_table_update_query += new_teamID
            teams_table_update_query += ' WHERE teamID = '
            teams_table_update_query += apostrophe
            teams_table_update_query += transmit[1]
            teams_table_update_query += apostrophe

            teams_table_update_query += ';' 
            print()
            print(teams_table_update_query)
            cursor.execute(teams_table_update_query)


            secondary_table_update_query = 'UPDATE teamshalf_teams SET teamID = '
            secondary_table_update_query += new_teamID
            secondary_table_update_query += ' WHERE teamID = '
            secondary_table_update_query += apostrophe
            secondary_table_update_query += transmit[1]
            secondary_table_update_query += apostrophe

            secondary_table_update_query += ';'
            print()
            print(secondary_table_update_query)
            cursor.execute(secondary_table_update_query)



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
            update_query += ';'
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
            indices_to_delete = [0, 3, 4]
            row[:] = [value for index, value in enumerate(row) if index not in indices_to_delete]

            data = list2dict(row, self.HEADER)         

            print("row is this: ", row)

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

            print("ilk satır: ", row)
            data = list2dict(row, self.teams_table_insertion_headers)


            teamshalf_table_insertion_headers = ['yearID', 'teamID', 'Half', 'DivWin', 'teamshalf.Rank', 'G', 'W', 'L']
            teamshalf_table_insertion_columns = ['int', 'str', 'str', 'str', 'int', 'int', 'int', 'int']


            secondary_table_insertion_headers =['teamID', 'lgID', 'divID', 'name']
            secondary_table_insertion_columns = ['str', 'str', 'str', 'str']


            teams_table_insert_query = 'INSERT INTO teams ('
            for i in self.teams_table_insertion_headers:
                if i == 'teamshalf.Half':
                    continue
                teams_table_insert_query += i + ', '
            teams_table_insert_query = teams_table_insert_query.removesuffix(', ')
            teams_table_insert_query += ') VALUES ('
            for i in range(len(self.teams_table_insertion_headers)):
                if self.teams_table_insertion_headers[i] == 'teamshalf.Half':
                    continue
                if data[self.teams_table_insertion_headers[i]] == 'None':
                    teams_table_insert_query += 'NULL'
                elif self.teams_table_insertion_column_types[i] == 'int':
                    teams_table_insert_query +=  data[self.teams_table_insertion_headers[i]] + ', '
                elif self.teams_table_insertion_column_types[i] == 'str':
                    teams_table_insert_query += '\'' + data[self.teams_table_insertion_headers[i]] + '\', '
            teams_table_insert_query = teams_table_insert_query.removesuffix(', ')
            teams_table_insert_query += ');'
            print()
            print(teams_table_insert_query)

            print("Table team insert query:", teams_table_insert_query)
            cursor.execute(teams_table_insert_query)
            


            indices_to_delete = [1, 5, 6, 7, 8, 9, 10]
            row_for_teamshalf_teams_secondary_table = [value for index, value in enumerate(row) if index not in indices_to_delete]
            element_to_move = row_for_teamshalf_teams_secondary_table.pop(0)
            row_for_teamshalf_teams_secondary_table.insert(3, element_to_move)

            print("Second row is this: ", row_for_teamshalf_teams_secondary_table)
            data2 = list2dict(row_for_teamshalf_teams_secondary_table, secondary_table_insertion_headers)

            secondary_table_insert_query = 'INSERT INTO teamshalf_teams ('
            for i in secondary_table_insertion_headers:
                secondary_table_insert_query += i + ', '
            secondary_table_insert_query = secondary_table_insert_query.removesuffix(', ')
            secondary_table_insert_query += ') VALUES ('
            for i in range(len(secondary_table_insertion_headers)):
                if data2[secondary_table_insertion_headers[i]] == 'None':
                    secondary_table_insert_query += 'NULL'
                elif secondary_table_insertion_columns[i] == 'int':
                    secondary_table_insert_query +=  data2[secondary_table_insertion_headers[i]] + ', '
                elif secondary_table_insertion_columns[i] == 'str':
                    secondary_table_insert_query += '\'' + data2[secondary_table_insertion_headers[i]] + '\', '
            secondary_table_insert_query = secondary_table_insert_query.removesuffix(', ')
            secondary_table_insert_query += ');'
            print()
            print(secondary_table_insert_query)

            print("Secondary table insert query:", secondary_table_insert_query)
            cursor.execute(secondary_table_insert_query)



            silinecek = [0, 3, 4]
            row_for_teamshalf_table = [value for index, value in enumerate(row) if index not in silinecek]

            print("Third row is this: ", row_for_teamshalf_table)
            data3 = list2dict(row_for_teamshalf_table, teamshalf_table_insertion_headers)


            insert_query = 'INSERT INTO teamshalf ('
            for i in teamshalf_table_insertion_headers:
                insert_query += i + ', '
            insert_query = insert_query.removesuffix(', ')
            insert_query += ') VALUES ('
            for i in range(len(teamshalf_table_insertion_headers)):
                if data3[teamshalf_table_insertion_headers[i]] == 'None':
                    insert_query += 'NULL'
                elif teamshalf_table_insertion_columns[i] == 'int':
                    insert_query +=  data3[teamshalf_table_insertion_headers[i]] + ', '
                elif teamshalf_table_insertion_columns[i] == 'str':
                    insert_query += '\'' + data3[teamshalf_table_insertion_headers[i]] + '\', '
            insert_query = insert_query.removesuffix(', ')
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