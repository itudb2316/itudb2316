from teamsHalf import TeamsHalf
import mysql.connector as dbapi
import maskPassword


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    
    def get_teamshalf_teams():
        teamshalf_teams = []
        with dbapi.connect(host="localhost", user="root", password=maskPassword.maskPsw(),database="lahman_2014")as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT name FROM teamshalf, teams WHERE teamshalf.teamID = teams.teamID")
            for row in cursor.fetchall():
                teamshalf_teams.append(row[0])
            cursor.close()
        return teamshalf_teams
    
    def get_teamshalf_info(team_name):
         with dbapi.connect(host="localhost", user="root", password=maskPassword.maskPsw(),database="lahman_2014")as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name, lgID, teamID, Half, divID, Rank, G, W, L FROM teamshalf, teams WHERE teamshalf.teamID = teams.teamID AND Half = 1 AND name = %s", (team_name,))
            first_half = cursor.fetchone()
            cursor.execute("SELECT name, lgID, teamID, Half, divID, Rank, G, W, L FROM teamshalf, teams WHERE teamshalf.teamID = teams.teamID AND Half = 2 AND name = %s", (team_name,))
            second_half = cursor.fetchone()
            cursor.close()
            return first_half, second_half
