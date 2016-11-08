"""Airfare search: https://github.com/wordswithchung/hackbright-project"""

import calendar
from datetime import date, datetime, timedelta
from flask import (Flask, jsonify, render_template, redirect,
                   request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import Airfare, Airport, connect_to_db, db
from sqlalchemy import func


app = Flask(__name__)

app.secret_key = "randomKeyGenerated1837492RandomKeyGeneratedLadidadidah00!!"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html", months=Airfare.calc_months())


@app.route('/search', methods=['POST'])
def search():
    """User searches for flight."""

    depart = request.form.get("depart")[:3] # string
    month, year = request.form.get("month").split() # int representing month year
    duration = request.form.get("duration") # int representing # of days

    duration, month, year = int(duration), int(month), int(year)

    month_name = calendar.month_name[month]
    user_port = Airport.query.filter_by(code=depart).first()

    airports = Airfare.choose_locations(month_name, user_port)
    start, end = Airfare.choose_dates(month, year, duration)

    return render_template("search.html",
                    kayak_urls=Airfare.make_kayak_urls(airports, start, end),
                    airports=airports,)


if __name__ == "__main__":
    # Debug to true while building and testing app
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=5000)