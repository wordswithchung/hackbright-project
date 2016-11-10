"""Airfare search: https://github.com/wordswithchung/hackbright-project"""
# native python
import calendar
from datetime import date, datetime, timedelta

# third-party
import flask
from flask import render_template, request
import flask_debugtoolbar
import jinja2

# my stuff
from model import Airfare, Airport, connect_to_db, db


app = flask.Flask(__name__)

app.secret_key = "randomKeyGenerated1837492RandomKeyGeneratedLadidadidah00!!"

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    months, month_names = Airfare.calc_months()

    return render_template("homepage.html",
                            months=months,
                            month_names=month_names,)


@app.route('/search', methods=['POST'])
def search():
    """User searches for flight."""

    depart = request.form.get("depart")[:3] # string
    month, year = request.form.get("month").split() # int representing month year
    duration = request.form.get("duration") # int representing # of days

    duration, month, year = int(duration), int(month), int(year)

    month_name = calendar.month_name[month]
    user_port = Airport.query.filter_by(code=depart).first()

    airfares = Airfare.choose_locations(month_name, user_port)
    start, end = Airfare.choose_dates(month, year, duration)

    return render_template("search.html",
                    kayak_urls=Airfare.make_kayak_urls(airfares, start, end),
                    airfares=airfares,
                    user_port=user_port,
                    month_name=month_name,
                    year=year,
                    duration=duration,)


if __name__ == "__main__":
    # Debug to true while building and testing app
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    flask_debugtoolbar.DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=5000)