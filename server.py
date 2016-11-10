"""Airfare search: https://github.com/wordswithchung/hackbright-project"""

import calendar
from datetime import date, datetime, timedelta

from flask import Flask, render_template, request, session
import flask_debugtoolbar
import jinja2

import db_func
import helper
import kayak
from model import Airfare, Airport, connect_to_db, db


app = Flask(__name__)

app.secret_key = "randomKeyGenerated1837492RandomKeyGeneratedLadidadidah00!!"

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    months, month_names = helper.calc_months()

    return render_template("homepage.html",
                            months=months,
                            month_names=month_names,)


@app.route('/search', methods=['POST'])
def search():
    """User searches for flight."""

    depart = request.form.get("depart")[:3] # string
    month, year = request.form.get("month").split() # int representing month year
    duration = request.form.get("duration") # int representing # of days

    session["depart"] = depart

    duration, month, year = int(duration), int(month), int(year)

    month_name = calendar.month_name[month]

    airfares = Airfare.choose_locations(month_name, depart)
    distances = db_func.calc_distance(airfares)
    start, end = helper.choose_dates(month, year, duration)

    return render_template("search.html",
                    kayak_urls=kayak.make_kayak_urls(airfares, start, end),
                    airfares=airfares,
                    month_name=month_name,
                    year=year,
                    duration=duration,
                    depart=depart,
                    distances=distances,)

@app.route('/sort-by-distance')
def sort_by_distance():
    """Sort results via AJAX from closest to furthest from depart code."""

    pass


if __name__ == "__main__":
    # Debug to true while building and testing app
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    flask_debugtoolbar.DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=5000)