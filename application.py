from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    return "registered"

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    session.clear()

    return render_template("login.html")

@app.route("/verification", methods=["GET"])
def ver():
    login = request.args.get("login")
    password = request.args.get("pass")

    if not login or not password:
        return jsonify(status="1")

    rows =  db.execute("SELECT * FROM users WHERE login = :username", username=login)

    if len(rows) != 1 or (password != rows[0]["pass"]):
        return jsonify(status="1")

    session["user_id"] = rows[0]["id"]

    print (session)

    return render_template("index.html")

@app.route("/tournaments")
def tournaments():
    return ""

@app.route("/new_tourn")
def new_tourn():
    return ""

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