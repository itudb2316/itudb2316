import mysql.connector as dbapi
from flask import current_app as app

class Fielding:
    INFO = {
        "fielding" : {
            'fm.playerID' : 'Player ID',
            'fm.yearID' : 'Year',
            'fm.stint' : 'Stint',
            'fm.pos' : 'Position',
            'fs.teamID' : 'Team',
            'fs.lgID' : 'League',
            'fm.g' : 'Games',
            'fm.gs' : 'Games Started',
            'fm.innOuts' : 'In Outs',
            'fm.po' : 'Putouts',
            'fm.a' : 'Assists',
            'fm.e' : 'Errors',
            'fm.dp' : 'Double Plays',
            'fm.pb' : 'Passed Balls',
            'fm.wp' : 'Wild Pitches',
            'fm.sb' : 'Stolen Bases',
            'fm.cs' : 'Caught Stealing',
            'fm.zr' : 'Zone Rating'
        },
    }

    TABLES = {
        "fielding" : {
            "main_cols" : {
                'g' : 'int',
                'gs' : 'int',
                'innOuts' : 'int',
                'po' : 'int',
                'a' : 'int',
                'e' : 'int',
                'dp' : 'int',
                'pb' : 'int',
                'wp' : 'int',
                'sb' : 'int',
                'cs' : 'int',
                'zr' : 'int'
            },
            "main_keys" : {
                'playerID' : 'str',
                'yearID' : 'int',
                'stint' : 'int',
                'pos' : 'str'
            },
            "sub_cols" : {
                'teamID' : 'str',
                'lgID' : 'str'
            },
            "sub_keys" : {
                'playerID' : 'str',
                'yearID' : 'int',
                'stint' : 'int'
            }
        },
        "fieldingpost" : {
            "main_cols" : {},
            "main_keys" : {},
            "sub_cols" : {},
            "sub_keys" : {}
        }
    }
    
    def __init__(self):
        self.app = app

    def view_fielding(self, queries, sort_by=None, order=None, exclude_null=True): 
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()
            #select_query = 'SELECT fm.*, fs.'
            select_query = 'SELECT fm.'
            select_query += ", fm.".join(self.TABLES["fielding"]["main_keys"].keys())
            select_query += ', fs.'
            select_query += ", fs.".join(self.TABLES["fielding"]["sub_cols"].keys())
            select_query += ', fm.'
            select_query += ", fm.".join(self.TABLES["fielding"]["main_cols"].keys())
            select_query += ' FROM fielding fm, fielding_sub fs WHERE'
            select_query += ' fm.playerID=fs.playerID AND fm.yearID=fs.yearID AND fm.stint=fs.stint AND '
            conditions = []
            print(queries.keys())
            for k,v in queries.items():
                if v == 'None' or v == None or v == 'Submit':
                    continue
                suffix = k.split('_')[0]
                field = k.split('_')[1]
                if suffix == 'mksk' or suffix == 'mk':
                    if self.TABLES["fielding"]["main_keys"][field] == 'int':
                        conditions.append('fm.' + field + ' = ' + v)
                    elif self.TABLES["fielding"]["main_keys"][field] == 'str':
                        conditions.append('fm.' + field + ' = \'' + v + '\'')
                elif suffix == 'mc':
                    if self.TABLES["fielding"]["main_cols"][field] == 'int':
                        conditions.append('fm.' + field + ' = ' + v)
                    elif self.TABLES["fielding"]["main_cols"][field] == 'str':
                        conditions.append('fm.' + field + ' = \'' + v + '\'')
                elif suffix == 'sk':
                    if self.TABLES["fielding"]["sub_keys"][field] == 'int':
                        conditions.append('fs.' + field + ' = ' + v)
                    elif self.TABLES["fielding"]["sub_keys"][field] == 'str':
                        conditions.append('fs.' + field + ' = \'' + v + '\'')
                elif suffix == 'sc':
                    if self.TABLES["fielding"]["sub_cols"][field] == 'int':
                        conditions.append('fs.' + field + ' = ' + v)
                    elif self.TABLES["fielding"]["sub_cols"][field] == 'str':
                        conditions.append('fs.' + field + ' = \'' + v + '\'')
            select_query += " AND ".join(conditions)
            if len(conditions) == 0:
                select_query = select_query.removesuffix('AND ')

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
            update_s_query = 'UPDATE fielding_sub AS fs SET '
            update_m_query = 'UPDATE fielding AS fm SET '
            print("NEW_DATA", new_data)
            
            conditions = []
            new_s_values = []
            new_m_values = []
            for k, v in new_data.items():
                if k.split('_')[0] == 'k':
                    if '\'' in v:
                        v = v.replace('\'', '\\\'')
                    if v == 'None' or v == None or v == '':
                        conditions.append(k.split('_')[2] + ' = NULL')
                    elif self.TABLES["fielding"]["main_keys"][k.split('_')[2]] == 'int':
                        conditions.append(k.split('_')[2] + ' = ' + v)
                    elif self.TABLES["fielding"]["main_keys"][k.split('_')[2]] == 'str':
                        conditions.append(k.split('_')[2] + ' = \'' + v + '\'')
                elif k.split('_')[0] == 'sc':
                    if '\'' in v:
                        v = v.replace('\'', '\\\'')
                    if v == 'None' or v == None or v == '':
                        new_s_values.append("fs." + k.split('_')[1] + ' = NULL')
                    elif self.TABLES["fielding"]["sub_cols"][k.split('_')[1]] == 'int':
                        new_s_values.append("fs." + k.split('_')[1] + ' = ' + v)
                    elif self.TABLES["fielding"]["sub_cols"][k.split('_')[1]] == 'str':
                        new_s_values.append("fs." + k.split('_')[1] + ' = \'' + v + '\'')
                elif k.split('_')[0] == 'mksk':
                    if '\'' in v:
                        v = v.replace('\'', '\\\'')
                    if v == 'None' or v == None or v == '':
                        new_m_values.append("fm." + k.split('_')[1] + ' = NULL')
                        new_s_values.append("fs." + k.split('_')[1] + ' = NULL')
                    elif self.TABLES["fielding"]["main_keys"][k.split('_')[1]] == 'int':
                        new_m_values.append("fm." + k.split('_')[1] + ' = ' + v)
                        new_s_values.append("fs." + k.split('_')[1] + ' = ' + v)
                    elif self.TABLES["fielding"]["main_keys"][k.split('_')[1]] == 'str':
                        new_m_values.append("fm." + k.split('_')[1] + ' = \'' + v + '\'')
                        new_s_values.append("fs." + k.split('_')[1] + ' = \'' + v + '\'')
                elif k.split('_')[0] == 'mk':
                    if '\'' in v:
                        v = v.replace('\'', '\\\'')
                    if v == 'None' or v == None or v == '':
                        new_m_values.append("fm." + k.split('_')[1] + ' = NULL')
                    elif self.TABLES["fielding"]["main_keys"][k.split('_')[1]] == 'int':
                        new_m_values.append("fm." + k.split('_')[1] + ' = ' + v)
                    elif self.TABLES["fielding"]["main_keys"][k.split('_')[1]] == 'str':
                        new_m_values.append("fm." + k.split('_')[1] + ' = \'' + v + '\'')
                elif k.split('_')[0] == 'mc':
                    if '\'' in v:
                        v = v.replace('\'', '\\\'')
                    if v == 'None' or v == None or v == '':
                        new_m_values.append("fm." + k.split('_')[1] + ' = NULL')
                    elif self.TABLES["fielding"]["main_cols"][k.split('_')[1]] == 'int':
                        new_m_values.append("fm." + k.split('_')[1] + ' = ' + v)
                    elif self.TABLES["fielding"]["main_cols"][k.split('_')[1]] == 'str':
                        new_m_values.append("fm." + k.split('_')[1] + ' = \'' + v + '\'')

            update_s_query += ", ".join(new_s_values)
            update_s_query += " WHERE "
            update_s_query += " AND ".join(conditions[:-1])

            update_m_query += ", ".join(new_m_values)
            update_m_query += " WHERE "
            update_m_query += " AND ".join(conditions)
            print()
            print(update_s_query)
            print(update_m_query)
            cursor.execute(update_s_query)
            cursor.execute(update_m_query)
            db.commit()
            cursor.close()
            db.close()
            return True
        except dbapi.Error as err:
            db.rollback()
            cursor.close()
            db.close()
            return False

    def delete_fielding(self, queries):
        try:
            db =  dbapi.connect(**self.app.config['MYSQL_CONN'])
            cursor = db.cursor()

            delete_m_query = f'DELETE FROM fielding WHERE playerID = \'{queries["mksk_playerID"]}\' AND '
            delete_m_query += f'yearID = {queries["mksk_yearID"]} AND '
            delete_m_query += f'stint = {queries["mksk_stint"]} AND '
            delete_m_query += f'pos = \'{queries["mk_pos"]}\';'

            print()
            print(delete_m_query)
            cursor.execute(delete_m_query)

            count_query = f'SELECT COUNT(*) FROM fielding WHERE playerID = \'{queries["mksk_playerID"]}\' AND '
            count_query += f'yearID = {queries["mksk_yearID"]} AND '
            count_query += f'stint = {queries["mksk_stint"]} AND '
            count_query += f'pos = \'{queries["mk_pos"]}\';'

            cursor.execute(count_query)
            num = int(cursor.fetchone()[0])
            print(count_query)
            print(num)

            if num == 0:
                delete_s_query = f'DELETE FROM fielding_sub WHERE playerID = \'{queries["mksk_playerID"]}\' AND '
                delete_s_query += f'yearID = {queries["mksk_yearID"]} AND '
                delete_s_query += f'stint = {queries["mksk_stint"]};'
                print(delete_s_query)
                cursor.execute(delete_s_query)
            
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
            m_cols = []
            s_cols = []
            m_vals = []
            s_vals = []
            for k, v in new_data.items():
                if k.split('_')[0] == 'mksk':
                    m_cols.append(k.split('_')[1])
                    s_cols.append(k.split('_')[1])
                    if v == 'None' or v == None or v == '':
                        m_vals.append('NULL')
                        s_vals.append('NULL')
                    elif self.TABLES["fielding"]["main_keys"][k.split('_')[1]] == 'int':
                        m_vals.append(v)
                        s_vals.append(v)
                    elif self.TABLES["fielding"]["main_keys"][k.split('_')[1]] == 'str':
                        m_vals.append('\'' + v + '\'')
                        s_vals.append('\'' + v + '\'')
                elif k.split('_')[0] == 'mk':
                    m_cols.append(k.split('_')[1])
                    if v == 'None' or v == None or v == '':
                        m_vals.append('NULL')
                    elif self.TABLES["fielding"]["main_keys"][k.split('_')[1]] == 'int':
                        m_vals.append(v)
                    elif self.TABLES["fielding"]["main_keys"][k.split('_')[1]] == 'str':
                        m_vals.append('\'' + v + '\'')
                elif k.split('_')[0] == 'mc':
                    m_cols.append(k.split('_')[1])
                    if v == 'None' or v == None or v == '':
                        m_vals.append('NULL')
                    elif self.TABLES["fielding"]["main_cols"][k.split('_')[1]] == 'int':
                        m_vals.append(v)
                    elif self.TABLES["fielding"]["main_cols"][k.split('_')[1]] == 'str':
                        m_vals.append('\'' + v + '\'')
                elif k.split('_')[0] == 'sc':
                    s_cols.append(k.split('_')[1])
                    if v == 'None' or v == None or v == '':
                        s_vals.append('NULL')
                    elif self.TABLES["fielding"]["sub_cols"][k.split('_')[1]] == 'int':
                        s_vals.append(v)
                    elif self.TABLES["fielding"]["sub_cols"][k.split('_')[1]] == 'str':
                        s_vals.append('\'' + v + '\'')
                

            insert_m_query = 'INSERT INTO fielding ('
            insert_m_query += ", ".join(m_cols)
            insert_m_query += ') VALUES ('
            insert_m_query += ", ".join(m_vals)
            insert_m_query += ');'
            cursor.execute(insert_m_query)

            insert_s_query = 'INSERT INTO fielding_sub ('
            insert_s_query += ", ".join(s_cols)
            insert_s_query += ') VALUES ('
            insert_s_query += ", ".join(s_vals)
            insert_s_query += ');'
            cursor.execute(insert_s_query)

            print(insert_m_query)
            print(insert_s_query)
            db.commit()
            cursor.close()
            db.close()
            return True
        except dbapi.Error as err:
            db.rollback()
            cursor.close()
            db.close()
            return False