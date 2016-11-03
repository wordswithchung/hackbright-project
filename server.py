"""Airfare search: https://github.com/wordswithchung/hackbright-project"""

import calendar
from datetime import date, datetime, timedelta
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

    today = datetime.today()
    months = [today]
    # http://stackoverflow.com/a/12736311
    
    for i in range(11):
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        month = today + timedelta(days=days_in_month)
        months.append(month)
        today = month
    
    return render_template("homepage.html", months=months)

@app.route('/search', methods=['POST'])
def search():
    """User searches for flight."""

    depart = request.form.get("depart")
    month = request.form.get("month")
    duration = request.form.get("duration")

    user_port = Port.query.filter_by(code=depart).first()



    print depart
    print month
    print duration



    ports_to_search = set()
    
@app.route('/autocomplete_port')
def autocomplete_airport_search():
    #https://designshack.net/articles/javascript/create-a-simple-autocomplete-with-html5-jquery/
    pass


if __name__ == "__main__":
    # Debug to true while building and testing app
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=5000)
