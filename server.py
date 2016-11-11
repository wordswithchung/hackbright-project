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

    # if session["depart"]:
    # Use Typeahead and set a default value for the aiport search box

    months, month_names = helper.calc_months()

    return render_template("homepage.html",
                            months=months,
                            month_names=month_names,)


@app.route('/search.json', methods=['POST'])
def search_json():
    """Take search terms and generate search results."""

    depart = request.form.get('depart')[:3]
    month, year = request.form.get('month').split()
    duration = request.form.get('duration')

    duration, month, year = int(duration), int(month), int(year)
    start, end = helper.choose_dates(month, year, duration)

    session["depart"] = depart

    airfares = Airfare.choose_locations(month, depart)
    distances = db_func.calc_distance(airfares)
    kayak_urls = kayak.make_kayak_urls(airfares, start, end)
    datas = zip(airfares, distances, kayak_urls)

    data = {}
    data['results'] = []
    for airfare, distance, kayak_url in datas:
        data['results'].append({
            'arrival_city'  : airfare.aport.city,
            'avg_price'     : int(airfare.average_price),
            'arrival_code'  : airfare.arrive,
            'distance'      : distance,
            'kayak_url'     : kayak_url
        })

    print data

    return jsonify(data)






if __name__ == "__main__":
    # Debug to true while building and testing app
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    flask_debugtoolbar.DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=5000)