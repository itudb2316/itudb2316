import mysql.connector as dbapi
from flask import current_app as app
from app.tools import list2dict

class Managers:

    COLUMNS = {
        'managerID': 'str',
        'yearID': 'int',
        'teamID': 'str',
        'lgID': 'str',
        'inseason': 'int',
        'G': 'int',
        'W': 'int',
        'L': 'int',
        'rank_': 'int',
        'plyrMgr': 'str'
    }

    COLUMNS_FOR_JOIN = {
        'managers_stats.managerID': 'str',
        'managers_stats.yearID': 'int',
        'managers_stats.teamID': 'str',
        'managers_lg.lgID': 'str',
        'managers_stats.inseason': 'int',
        'managers_stats.G': 'int',
        'managers_stats.W': 'int',
        'managers_stats.L': 'int',
        'managers_lg.rank_': 'int',
        'managers_player.plyrMgr': 'str'
    }

    managers_stats_COLUMNS = {
        'managers_stats.managerID': 'str',
        'managers_stats.yearID': 'int',
        'managers_stats.teamID': 'str',
        'managers_stats.inseason': 'int',
        'managers_stats.G': 'int',
        'managers_stats.W': 'int',
        'managers_stats.L': 'int'
    }

    managers_stats_insert_COLUMNS = {
        'managerID': 'str',
        'yearID': 'int',
        'teamID': 'str',
        'inseason': 'int',
        'G': 'int',
        'W': 'int',
        'L': 'int'
    }

    managers_lg_COLUMNS = {
        'managers_lg.yearID': 'int',
        'managers_lg.teamID': 'str',
        'managers_lg.rank_': 'int',
        'managers_lg.lgID': 'str'
    }

    managers_lg_insert_COLUMNS = {
        'yearID': 'int',
        'teamID': 'str',
        'rank_': 'int',
        'lgID': 'str'        
    }

    managers_player_COLUMNS = {
        'managers_player.managerID': 'str',
        'managers_player.yearID': 'int',
        'managers_player.plyrMgr': 'str'
    }

    managers_player_insert_COLUMNS = {
        'managerID': 'str',
        'yearID': 'int',
        'plyrMgr': 'str'
    }

    def __init__(self):
        self.app = app

    def view_managers(self, queries, sort_by=None, order=None, exclude_null=True): 
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()

            select_query = 'SELECT '
            select_query += ", ".join(self.COLUMNS_FOR_JOIN.keys())
            select_query += ' FROM managers_stats JOIN managers_lg ON managers_stats.yearID = managers_lg.yearID and managers_stats.teamID = managers_lg.teamID JOIN managers_player ON managers_stats.managerID = managers_player.managerID and managers_stats.yearID = managers_player.yearID WHERE '
            
            conditions = []

            print(queries) 

            for k,v in queries.items():
                if v == 'None' or v == None:
                    continue
                if self.COLUMNS[k] == 'int':
                    if k in ['managerID','yearID', 'teamID', 'inseason', 'G', 'W', 'L']:
                        conditions.append("managers_stats." + k + ' = ' + str(v))
                    if k in ['rank_', 'lgID']:
                        conditions.append("managers_lg." + k + ' = ' + str(v))            
                    if k in ['plyrMgr']:
                        conditions.append("managers_player." + k + ' = ' + str(v))

                elif self.COLUMNS[k] == 'str':
                    if k in ['managerID','yearID', 'teamID', 'inseason', 'G', 'W', 'L']:
                        conditions.append("managers_stats." + k + ' = \'' + v + '\'')
                    if k in ['rank_', 'lgID']:
                        conditions.append("managers_lg." + k + ' = \'' + v + '\'')
                    if k in ['plyrMgr']:
                        conditions.append("managers_player." + k + ' = \'' + v + '\'')

            select_query += " AND ".join(conditions)

            if len(conditions) == 0:
                select_query = select_query.removesuffix('WHERE ')

            if sort_by != None:
                if sort_by == 'managerID':
                    sort_by = 'managers_stats.managerID'

                elif sort_by == 'teamID':
                    sort_by = 'managers_stats.teamID'

                elif sort_by == 'yearID':
                    sort_by = 'managers_stats.yearID'

                select_query += ' ORDER BY '
                if exclude_null:
                    select_query += 'CASE WHEN ' + sort_by + ' IS NULL THEN 1 ELSE 0 END, '
                
                select_query += sort_by + ' ' + order
            
            select_query += ';'

            print()
            print(select_query)
            cursor.execute(select_query)
            results = cursor.fetchall()

            #print(results)
            db.commit()
            
        except dbapi.Error as err:
            db.rollback()
            results = []

        finally:
            cursor.close()
            db.close()

        return results
    
    def update_managers(self, oldmanagerID, oldyearID, oldteamID, oldinseason, new_data):
        try:
            print("buradaa")
            print(oldmanagerID)
            print(oldyearID)
            print(oldteamID)
            print(oldinseason)

            print(new_data)

            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()

            # Update managers_stats table
            update_query = 'UPDATE managers_stats SET '

            print("NEW_DATA", new_data)
            
            new_values = []
            for k,v in new_data.items():
                if k in Managers.managers_stats_insert_COLUMNS:
                    if '\'' in v:
                        v = v.replace('\'', '\\\'')
                    if v == 'None' or v == None:
                        new_values.append("managers_stats." + k + ' = NULL')
                    elif self.COLUMNS[k] == 'int':
                        new_values.append("managers_stats." + k + ' = ' + v)
                    elif self.COLUMNS[k] == 'str':
                        new_values.append("managers_stats." + k + ' = \'' + v + '\'')
            update_query += ", ".join(new_values)
            #update_query += ' WHERE managers_stats.managerID = \'' + oldmanagerID + '\' AND managers_stats.yearID = ' + str(oldyearID) + ' AND managers_stats.teamID = \'' + oldteamID + '\' AND managers_stats.inseason = ' + str(oldinseason) + ';'
            update_query += ' WHERE managers_stats.yearID = ' + str(oldyearID) + ' AND managers_stats.teamID = \'' + oldteamID + '\' AND managers_stats.inseason = ' + str(oldinseason) + ';'

            print()
            print(update_query)
            cursor.execute(update_query)

            # Update managers_lg table
            update_query = 'UPDATE managers_lg SET '

            print("NEW_DATA", new_data)
            
            new_values = []
            for k,v in new_data.items():
                if k in Managers.managers_lg_insert_COLUMNS:
                    if '\'' in v:
                        v = v.replace('\'', '\\\'')
                    if v == 'None' or v == None:
                        new_values.append("managers_lg." + k + ' = NULL')
                    elif self.COLUMNS[k] == 'int':
                        new_values.append("managers_lg." + k + ' = ' + v)
                    elif self.COLUMNS[k] == 'str':
                        new_values.append("managers_lg." + k + ' = \'' + v + '\'')
            update_query += ", ".join(new_values)
            update_query += ' WHERE managers_lg.yearID = ' + str(oldyearID) + ' AND managers_lg.teamID = \'' + oldteamID + '\';'


            print()
            print(update_query)
            cursor.execute(update_query)


            # Update managers_player table
            update_query = 'UPDATE managers_player SET '

            print("NEW_DATA", new_data)
            
            new_values = []
            for k,v in new_data.items():
                if k in Managers.managers_player_insert_COLUMNS:
                    if '\'' in v:
                        v = v.replace('\'', '\\\'')
                    if v == 'None' or v == None:
                        new_values.append("managers_player." + k + ' = NULL')
                    elif self.COLUMNS[k] == 'int':
                        new_values.append("managers_player." + k + ' = ' + v)
                    elif self.COLUMNS[k] == 'str':
                        new_values.append("managers_player." + k + ' = \'' + v + '\'')
            update_query += ", ".join(new_values)
            update_query += ' WHERE managers_player.managerID = \'' + oldmanagerID + '\' AND managers_player.yearID = ' + str(oldyearID) + ';'


            print()
            print(update_query)
            cursor.execute(update_query)

            results = cursor.fetchall()
            db.commit()
            successFlag = True
            
        except dbapi.Error as err:
            db.rollback()
            results = []
            successFlag = False

        finally:
            cursor.close()
            db.close()
        return results, successFlag
        
    def delete_managers(self, managerID, yearID, teamID, inseason):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()

            print(managerID)
            print(yearID)
            print(inseason)
            print(teamID)

            # Delete manager from manager_stats 
            # delete_query = 'DELETE FROM managers_stats WHERE managers_stats.managerID = \'' + managerID + '\' AND managers_stats.yearID = ' + str(yearID) + ' AND managers_stats.teamID = \'' + teamID + '\' AND managers_stats.inseason = ' + str(inseason) + ';'
            delete_query = 'DELETE FROM managers_stats WHERE managers_stats.yearID = ' + str(yearID) + ' AND managers_stats.teamID = \'' + teamID + '\' AND managers_stats.inseason = ' + str(inseason) + ';'
            
            print()
            print(delete_query)

            cursor.execute(delete_query)

            # Delete manager from managers_player
            delete_query = 'DELETE FROM managers_player WHERE managers_player.managerID = \'' + managerID + '\' AND managers_player.yearID = ' + str(yearID) + ';'

            print()
            print(delete_query)

            cursor.execute(delete_query)

            # Delete manager from managers_lg
            delete_query = 'DELETE FROM managers_lg WHERE managers_lg.yearID = ' + str(yearID) + ' AND managers_lg.teamID = \'' + teamID + '\';'
            
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

            print("NEWW DATAA")
            print(new_data)
            print()

            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()

            managers = app.config['MANAGERS']
            
            # Insert to managers_stats table
            insert_query = 'INSERT INTO managers_stats ('
            

            insert_query += ", ".join(managers.managers_stats_COLUMNS.keys())
                                #.join([column_name for column_name in managers.COLUMNS.keys()
                                       #if column_name != 'lahmanID']) #primary key

            insert_query += ') VALUES ( '
            
            values = []
            for k,v in managers.managers_stats_insert_COLUMNS.items():
                
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


            # Insert to managers_lg table
            insert_query = 'INSERT INTO managers_lg ('
            

            insert_query += ", ".join(managers.managers_lg_COLUMNS.keys())
                                #.join([column_name for column_name in managers.COLUMNS.keys()
                                       #if column_name != 'lahmanID']) #primary key

            insert_query += ') VALUES ( '
            
            values = []
            for k,v in managers.managers_lg_insert_COLUMNS.items():
                
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

            # Insert to managers_player table
            insert_query = 'INSERT INTO managers_player ('
            

            insert_query += ", ".join(managers.managers_player_COLUMNS.keys())
                                #.join([column_name for column_name in managers.COLUMNS.keys()
                                       #if column_name != 'lahmanID']) #primary key

            insert_query += ') VALUES ( '
            
            values = []
            for k,v in managers.managers_player_insert_COLUMNS.items():
                
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

    def winner(self, queries):    
            try:
                db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
                cursor = db.cursor()
                
                managerID = queries['managerID']


                stored_function_query = 'SELECT DISTINCT managers_stats.managerID, GetManagerWinPercentage(managers_stats.managerID) AS winPercentage FROM managers_stats WHERE managers_stats.managerID = \'' + managerID + '\' ;'
            
                cursor.execute(stored_function_query)

                results = cursor.fetchall()
                
                db.commit()

            except dbapi.Error as err:
                db.rollback()
                results = []
                
            finally:
                cursor.close()
                db.close()

            return results
    
    def champions(self):    
            try:
                db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
                cursor = db.cursor()
                
                stored_procedure_query = 'call GetChampionsLast20Years();'
            
                cursor.execute(stored_procedure_query)

                results = cursor.fetchall()

            except dbapi.Error as err:
                db.rollback()
                results = []
                
            finally:
                cursor.close()
                db.close()

            return results
    
    def legends(self):    
            try:
                db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
                cursor = db.cursor()
                
                stored_procedure_query = 'call GetMostExperiencedManagers();'
            
                cursor.execute(stored_procedure_query)

                results = cursor.fetchall()

            except dbapi.Error as err:
                db.rollback()
                results = []
                
            finally:
                cursor.close()
                db.close()

            return results