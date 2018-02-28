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
    return render_template("home.html")

@app.route("/tournaments")
#@login_required
def tournaments():

    try:
        tournament = db.execute("SELECT * FROM tournaments JOIN locations on tournaments.location_id = id")

        return render_template("tournaments.html", roster=tournament)
    except:
        return "Exeption on dtb"

@app.route("/new_tourn", methods=["GET", "POST"])
def new_tourn():
    if request.method == "POST":
        players = 0

        try:
            players = request.form.getlist("pla")
            print (players[0])
        except:
            print (players)


        return jsonify(players)
    else:
        return render_template("new_tourn.html")

@app.route("/games")
def games():
    return ""

@app.route("/new_game")
def new_game():
    return ""

@app.route("/new_player")
def new_player():
    return ""

@app.route("/players")
def players():
    return ""