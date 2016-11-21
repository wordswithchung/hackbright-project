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

    session["depart"] = request.form.get('depart')

    airfares = Airfare.choose_locations(month, depart)
    distances = db_func.calc_distance(airfares)
    kayak_urls = kayak.make_kayak_urls(airfares, start, end)
    data = zip(airfares, distances, kayak_urls)

    info = []
    for airfare, distance, kayak_url in data:
        info.append({
            'arrival_city'  : airfare.aport.city,
            'avg_price'     : int(airfare.average_price),
            'airport_code'  : airfare.arrive,
            'distance'      : distance,
            'kayak_url'     : kayak_url
        })

    return render_template('search.html', info=info,
                                          length=len(kayak_urls),
                                          depart=depart,
                                          year=year,
                                          month=calendar.month_name[month],
                                          duration=duration,)


@app.route('/map')
def map():
    """Render a Google Map that displays the airfare database info."""

    # this can probably go in db_func when I refactor the code
    airfares = {}
    airport_latlngs = {}
    for airfare in Airfare.query.all():
        a = airfare.depart
        if a in airfares:
            airfares[a].append({
                             "arrival_city": airfare.arrive,
                             "city_name": airfare.aport.city,
                             "arrival_lat": airfare.aport.lat,
                             "arrival_lng": airfare.aport.lng,
                             "avg_price": airfare.average_price,
                             "cheapest_month": airfare.cheapest_month,})
        else:
            airfares[a] = []
            airport_latlngs[a] = (airfare.dport.lat, airfare.dport.lng)

    return render_template('map.html', airfares=airfares,
                                       airport_latlngs=airport_latlngs,)



if __name__ == "__main__":
    # Debug to true while building and testing app
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    flask_debugtoolbar.DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=5000)