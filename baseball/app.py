from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import maskPassword
from search import SearchForm
from flask_wtf import CSRFProtect

app = Flask("__name__")

csrf = CSRFProtect(app)
app.secret_key = "hcq94qhf394f0bu80q82093r"  # used in csfr token

# Your database configuration
# Create a MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # root in default
    password=maskPassword.maskPsw(),  # your mySQL password written in maskPassword.py file!
    database="lahman_2014",  # the database created in mySQL and it is in use (mySQL is UP!)
)
# Create a cursor to interact with the database and manipulate
cursor = db.cursor()


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/player", methods=["GET", "POST"])
def player_search():
    form = SearchForm()
    if request.method == "POST" and form.validate_on_submit():
        return redirect((url_for("player_info", query=form.search.data)))
    return render_template("player.html", form=form)


@app.route("/player/<query>")
def player_info(query):
    select_query = "SELECT nameFirst, nameLast, height, weight, bats, throws FROM players WHERE nameFirst = '{}' AND nameLast = '{}'".format(
        query.split(" ")[0], query.split(" ")[1]
    )

    cursor.execute(select_query)
    result = cursor.fetchall()

    results = []
    for row in result:
        results.append(
            {
                "fname": row[0],
                "lname": row[1],
                "height": row[2],
                "weight": row[3],
                "bats": row[4],
                "throws": row[5],
            }
        )

    if len(results) == 0:
        return redirect(url_for("player_search"))
    return render_template("player_info.html", results=results)


if __name__ == "__main__":
    app.run()
