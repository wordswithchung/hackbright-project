"""Airfare search: https://github.com/wordswithchung/hackbright-project"""

import calendar
from datetime import date, datetime, timedelta

from flask import Flask, jsonify, render_template, request, session
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
    """Render search results."""

    depart = request.form.get('depart')[:3]
    month, year = request.form.get('month').split()
    duration = request.form.get('duration')

    duration, month, year = int(duration), int(month), int(year)
    start, end = helper.choose_dates(month, year, duration)
    airfares = Airfare.choose_locations(month, depart)
    distances = db_func.calc_distance(airfares)
    kayak_urls = kayak.make_kayak_urls(airfares, start, end)
    info = db_func.create_search_result_obj(airfares, distances, kayak_urls)

    return render_template('search.html', info=info,
                                          length=len(kayak_urls),
                                          depart=depart,
                                          year=year,
                                          month=calendar.month_name[month],
                                          duration=duration,)


@app.route('/map')
def map():
    """Render a Google Map that displays the airfare database info."""

    airfares = Airfare.create_map_airfare_objs()

    return render_template('map.html', airfares=airfares)


if __name__ == "__main__":
    # Debug to true while building and testing app
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # flask_debugtoolbar.DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=5000)