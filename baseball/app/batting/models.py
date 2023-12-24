import mysql.connector as dbapi
from flask import current_app as app

class Batting:
    
    header_type = {
        'mksk_playerID': 'str',
        'mksk_yearID': 'int',
        'mksk_stint': 'int',
        'sc_teamID': 'str',
        'sc_lgID': 'str',
        'mk_G': 'int',
        'mk_AB': 'int',
        'mk_R': 'int',
        'mk_H': 'int',
        'mk_2B': 'int',
        'mk_3B': 'int',
        'mk_HR': 'int',
        'mk_RBI': 'int',
        'mk_SB': 'int',
        'mk_CS': 'int',
        'mk_BB': 'int',
        'mk_SO': 'int',
        'mk_IBB': 'int',
        'mk_HBP': 'int',
        'mk_SH': 'int',
        'mk_SF': 'int',
        'mk_GIDP': 'int'
    }
    
    INFO = {
        "batting": {
            'batting.playerID': 'Player ID',
            'batting.yearID': 'Year ID',
            'batting.stint': 'Stint',
            'batting_teams.teamID': 'Team ID',
            'batting_teams.lgID': 'League ID',
            'batting.G': 'Games',
            'batting.AB': 'At bats',
            'batting.R': 'Runs',
            'batting.H': 'Hits',
            'batting.2B': 'Doubles',
            'batting.3B': 'Triples',
            'batting.HR': 'Home runs',
            'batting.RBI': 'Runs batted in',
            'batting.SB': 'Stolen bases',
            'batting.CS': 'Caught stealing',
            'batting.BB': 'Base on balls',
            'batting.SO': 'Strikeouts',
            'batting.IBB': 'Intentional walks',
            'batting.HBP': 'Hits by pitch',
            'batting.SH': 'Sacrifice hits',
            'batting.SF': 'Sacrifice flies',
            'batting.GIDP': 'Plays grounded by double play'
        },
    }
    
    TABLES = {
        "batting" : {
            "main_cols" : {
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
                'BB': 'int',
                'SO': 'int',
                'IBB': 'int',
                'HBP': 'int',
                'SH': 'int',
                'SF': 'int',
                'GIDP': 'int'
            },
            "main_keys" : {
                'playerID' : 'str',
                'yearID' : 'int',
                'stint' : 'int'
            },
            "sub_cols" : {
                'teamID' : 'str',
                'lgID' : 'str'
            },
            "sub_keys" : {
                'playerID' : 'str',
                'yearID' : 'int',
                'stint' : 'int'
            },
            "batting_cols": {
                'batting.playerID': 'str',
                'batting.yearID': 'int',
                'batting.stint': 'int',
                'batting.teamID': 'str',
                'batting.lgID': 'str',
                'batting.G': 'int',
                'batting.AB': 'int',
                'batting.R': 'int',
                'batting.H': 'int',
                'batting.2B': 'int',
                'batting.3B': 'int',
                'batting.HR': 'int',
                'batting.RBI': 'int',
                'batting.SB': 'int',
                'batting.CS': 'int',
                'batting.BB': 'int',
                'batting.SO': 'int',
                'batting.IBB': 'int',
                'batting.HBP': 'int',
                'batting.SH': 'int',
                'batting.SF': 'int',
                'batting.GIDP': 'int'                
            },
            "batting_teams_cols": {
                'batting_teams.playerID': 'str',
                'batting_teams.yearID': 'int',
                'batting_teams.stint': 'int',
                'batting_teams.teamID': 'str',
                'batting_teams.lgID': 'str'
            },
            "batting_insert": {
                'mksk_playerID': 'str',
                'mksk_yearID': 'int',
                'mksk_stint': 'int',
                'sc_teamID': 'str',
                'sc_lgID': 'str',
                'mk_G': 'int',
                'mk_AB': 'int',
                'mk_R': 'int',
                'mk_H': 'int',
                'mk_2B': 'int',
                'mk_3B': 'int',
                'mk_HR': 'int',
                'mk_RBI': 'int',
                'mk_SB': 'int',
                'mk_CS': 'int',
                'mk_BB': 'int',
                'mk_SO': 'int',
                'mk_IBB': 'int',
                'mk_HBP': 'int',
                'mk_SH': 'int',
                'mk_SF': 'int',
                'mk_GIDP': 'int'
            },
            "batting_teams_insert": {
                'mksk_playerID': 'str',
                'mksk_yearID': 'int',
                'mksk_stint': 'int',
                'sc_teamID': 'str',
                'sc_lgID': 'str'
            }
        },
        "battingpost" : {
            "main_cols" : {},
            "main_keys" : {},
            "sub_cols" : {},
            "sub_keys" : {}
        }
    }
    
    def __init__(self):
        self.app = app
        
    def view_batting(self, queries, sort_by=None, order=None, exclude_null=True):
        try:
            db = dbapi.connect(**self.app.config['MYSQL_CONN']) #**self.app.config['MYSQL_CONN']
            cursor = db.cursor()
            select_query = 'SELECT bm.'
            select_query += ", bm.".join(self.TABLES["batting"]["main_keys"].keys())
            select_query += ', bs.'
            select_query += ", bs.".join(self.TABLES["batting"]["sub_cols"].keys())
            select_query += ', bm.'
            select_query += ", bm.".join(self.TABLES["batting"]["main_cols"].keys())
            select_query += ' FROM batting bm, batting_teams bs WHERE'
            select_query += ' bm.playerID=bs.playerID AND bm.yearID=bs.yearID AND bm.stint=bs.stint AND '
            conditions = []
            for k,v in queries.items():
                if v == 'None' or v == None or v == 'Submit':
                    continue
                print(k)
                suffix = k.split('_')[0]
                field = k.split('_')[1]
                if suffix == 'mksk':
                    if self.TABLES["batting"]["main_keys"][field] == 'int':
                        conditions.append('bm.' + field + ' = ' + v)
                    elif self.TABLES["batting"]["main_keys"][field] == 'str':
                        conditions.append('bm.' + field + ' = \'' + v + '\'')
                elif suffix == 'mc':
                    if self.TABLES["batting"]["main_cols"][field] == 'int':
                        conditions.append('bm.' + field + ' = ' + v)
                    elif self.TABLES["batting"]["main_cols"][field] == 'str':
                        conditions.append('bm.' + field + ' = \'' + v + '\'')
                elif suffix == 'sk':
                    if self.TABLES["batting"]["sub_keys"][field] == 'int':
                        conditions.append('bs.' + field + ' = ' + v)
                    elif self.TABLES["batting"]["sub_keys"][field] == 'str':
                        conditions.append('bs.' + field + ' = \'' + v + '\'')
                elif suffix == 'sc':
                    if self.TABLES["batting"]["sub_cols"][field] == 'int':
                        conditions.append('bs.' + field + ' = ' + v)
                    elif self.TABLES["batting"]["sub_cols"][field] == 'str':
                        conditions.append('bs.' + field + ' = \'' + v + '\'')
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
            
    def insert_batting(self, data):
        try:
            print(data)
            db = dbapi.connect(**self.app.config['MYSQL_CONN']) 
            cursor = db.cursor()
            insert_query = 'INSERT INTO batting ('
            insert_query += ", ".join(self.TABLES["batting"]["batting_cols"].keys())
            insert_query += ') VALUES ( '
            
            values = []
            for k,v in self.TABLES["batting"]["batting_insert"].items():
                
                print(k)
                
                if(k not in data.keys()):
                    values.append("NULL")
                    continue
                
                value = data[k]
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
            print(insert_query)
            cursor.execute(insert_query)
            
            insert_query = 'INSERT INTO batting_teams ('
            insert_query += ", ".join(self.TABLES["batting"]["batting_teams_cols"].keys())
            insert_query += ') VALUES ( '
            
            values = []
            for k,v in self.TABLES["batting"]["batting_teams_insert"].items():

                if(k not in data.keys()):
                    values.append("NULL")
                    continue
                
                value = data[k]
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

    def update_batting(self, keys, data):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            update_query = 'UPDATE batting SET '
            conditions = []
            for k,v in data.items():
                if v == 'None' or v == None:
                    conditions.append(k + '= NULL')
                if self.header_type[k] == 'int':
                    conditions.append(k + ' = ' + v)
                elif self.header_type[k] == 'str':
                    conditions.append(k + ' = \'' + v + '\'')
            update_query += ', '.join(conditions)
            update_query += ' WHERE playerID = \'' + keys[0] + '\' AND yearID = ' + keys[1] + ' AND stint = ' + keys[2]
            print()
            print(update_query)
            cursor.execute(update_query)
            result = cursor.fetchall()
            db.commit()
        except dbapi.Error as err:
            db.rollback()
            result = []
        finally:
            cursor.close()
            db.close()
        return result
            
    def delete_batting(self, keys):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            delete_query = 'DELETE FROM batting WHERE playerID = \'' + keys[0] + '\' AND yearID = ' + keys[1] + ' AND stint = ' + keys[2]
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