from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cachedasdas
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///TGP_data.db")

@app.template_filter("datetimeformat")
def datetimeformat(value, format="%Y-%m-%d"):
    date = datetime.strptime(value, format)
    return date.strftime("%d.%m.%Y")

app.jinja_env.filters["datetimeformat"] = datetimeformat

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("username"):
            return print("Missing username!")

        # ensure password was provided
        elif not request.form.get("password"):
            return print("Must provide password")

        # ensure password was confirmed
        elif not request.form.get("c_password"):
            return print("Must confirm password")

        elif request.form.get("password") != request.form.get("c_password"):
            return print("Password does not match confirmation")

        hash_pwd = pwd_context.hash(request.form.get("password"))

        result = db.execute("INSERT INTO users (login, hash) VALUES (:username, :hash_pwd)",
                            username=request.form.get("username"), hash_pwd=hash_pwd)

        if not result:
            return print("The username has been already taken, please try with another one")

        # remember login the user has logged in
        session["user_id"] = result

        # redirect user to home page
        return redirect(url_for("home"))

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    session.clear()

    if request.method == "POST":
        login = request.form["login"]
        password = request.form["inputPassword1"]

        print (login)

        if not login or not password:
            return jsonify(status="1")

        rows =  db.execute("SELECT * FROM users WHERE login = :username", username=login)

        if len(rows) != 1 or not pwd_context.verify(password, rows[0]["hash"]):
            return jsonify(status="2")

        session["user_id"] = rows[0]["id"]

        return redirect(url_for("home"))

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("index"))

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return redirect(url_for("tournaments"))

@app.route("/tournaments")
@login_required
def tournaments():

    tournament = db.execute("SELECT * FROM tournaments JOIN locations on tournaments.location_id = l_id")
    return render_template("tournaments.html", roster=tournament)

    try:
        tournament = db.execute("SELECT * FROM tournaments JOIN locations on tournaments.location_id = l_id")
        return render_template("tournaments.html", roster=tournament)
    except:
        return "Exeption on dtb 1"

@app.route("/new_tourn", methods=["GET", "POST"])
@login_required
def new_tourn():
    if request.method == "POST":

        players = request.form.getlist("pla")
        players = [tuple(p.split(",")) for p in players]
        date = request.form["date"]
        max_players = request.form["max"]
        location = request.form["location"]

        print (players, date, max_players, location)

        try:
            t_id = db.execute("INSERT INTO tournaments (date, max_num, location_id, t_type_id) VALUES (:date, :max_num, 1, 1)",
                            date=date, max_num=max_players)
        except:
            print ("Error 1")

        try:
            for p in players:
                db.execute("INSERT INTO participants (t_id, p1, p2) VALUES (:t_id, :p1, :p2)",
                t_id=t_id, p1=p[0], p2=p[1])
        except:
            print ("error 2")

        return redirect(url_for("tournament",t_id=t_id))
    else:
        t_id = request.args.get("t_id")

        tournament = db.execute("SELECT t_id, date, p1, p2, max_num, location FROM participants JOIN tournaments ON participants.t_id = id JOIN locations ON tournaments.location_id = locations.l_id WHERE t_id = :t_id",
                            t_id=t_id)
        return render_template("new_tourn.html", roster=tournament)

@app.route("/tournament")
@login_required
def tournament(t_id=None):

    if t_id is None:
        t_id = request.args.get("t_id")

    print (t_id)

    tournament = db.execute("SELECT t_id, date, p1, p2, max_num, location FROM participants JOIN tournaments ON participants.t_id = id JOIN locations ON tournaments.location_id = locations.l_id WHERE t_id = :t_id",
                            t_id=t_id)

    return render_template("tournament.html", roster=tournament)

    # try:
    #     tournament = db.execute("SELECT t_id, p1, p2 FROM participants JOIN tournaments ON participants.t_id = id WHERE t_id = :t_id",
    #     t_id=t_id)
    #     return render_template("tournament.html", roster=tournament)
    # except:
    #     return redirect("/tournaments")

@app.route("/games")
def games():
    # YET TO DO
    return ""

@app.route("/new_game")
def new_game():
    # YET TO DO
    return ""

@app.route("/new_player")
def new_player():
    # YET TO DO
    return ""

@app.route("/players")
def players():
    # YET TO DO
    return ""