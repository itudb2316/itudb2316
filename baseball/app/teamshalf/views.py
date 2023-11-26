from flask import Flask, render_template, request, redirect, url_for
from search import SearchForm
from database import Database as db

app = Flask("__name__")


@app.route("/teamshalf")
def teamshalf_team_selection():
    teams = db.get_teamshalf_teams()
    return render_template("teamshalf.html", teams = teams)


@app.route('/teamshalf/team_stats', methods=['GET','POST'])
def teamshalf_team_stats():
    team_name = request.form.get('team_name')
    first_half, second_half = db.get_teamshalf_info(team_name)
    return render_template('teamshalf_team_stats.html', team_name = team_name, first_half=first_half, second_half = second_half)