from cs50 import SQL
from flask import redirect, render_template, request, session, url_for
from functools import wraps


# configure CS50 Library to use SQLite database
db = SQL("sqlite:///TGP_data.db")

def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
# not used
def create_new_tournament():
    return True

# adds new tournamen to SQLlite database
def add_tournament(max_players, date, players):

    try:
        t_id = db.execute("INSERT INTO tournaments (date, max_num, location_id, t_type_id) VALUES (:date, :max_num, 1, 1)",
                            date=date, max_num=max_players)
    except:
        print ("Error creating a new tournament")
        return redirect(url_for("tournaments"))


    # add players to the tournament
    if update_players(players, t_id):
        return redirect(url_for("tournament",t_id=t_id))
    else:
        print("error, filed to update players for tournamet {}".format(t_id))
        return redirect(url_for("tournaments")) # add error handle here

# updates tournament
def update_tournament(tourn_id, max_players, date_t, players):

    # update tournament with new date, location and max num of players
    db.execute("UPDATE tournaments SET date=:date, max_num=:max_num, location_id=1, t_type_id=1 WHERE id=:t_id", date=date_t, max_num=max_players, t_id=tourn_id)

    # delete players for this tournament
    try:
        db.execute("DELETE FROM participants WHERE t_id=:t_id", t_id=tourn_id)
    except:
        print("Failed to delet players from tournament #{}".format(tourn_id))
        pass

    if update_players(players, tourn_id):
        return redirect(url_for("tournament",t_id=tourn_id))
    else:
        return "" # add error handle here


# updates players of a tournament
def update_players(players, t_id):
    try:
        for p in players:
            db.execute("INSERT INTO participants (t_id, p1, p2) VALUES (:t_id, :p1, :p2)",
            t_id=t_id, p1=p[0], p2=p[1])
        return True
    except:
        print("error, failed to update players for tournament {}".format(t_id))
        # return redirect(url_for("tournaments")
        return False