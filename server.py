"""Airfare search: https://github.com/wordswithchung/hackbright-project"""

from datetime import datetime
from flask import (Flask, jsonify, render_template, redirect, 
                   request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import Airfare, Port, connect_to_db, db
from sqlalchemy import func


app = Flask(__name__)

app.secret_key = "randomKeyGenerated1837492RandomKeyGeneratedLadidadidah00!!"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")

@app.route('/search', methods=['POST'])
def search():
    """User searches for flight."""

    # depart = request.form.get("depart")
    # month = request.form.get("month")
    # duration = request.form.get("duration")

    # things to implement: depart should pull from airports database
    # for autocomplete

    """LOGIC V2

    When we get user's depart and month:
    - if depart exists in airfares table (Airfare), find the best $/mile
    and ping the API for those arrival airport codes
    - in addition, find the arrival airport codes which has the cheapest_
    month equal to user's month. Diversify the distance from user's depart
    and ping the API for those arrival airport codes
    """

    # SECTION ONE ######
    user_port = Port.query.filter_by(code=depart).first()

    ports_to_search = set()
    



if __name__ == "__main__":
    # Debug to true while building and testing app
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000)
