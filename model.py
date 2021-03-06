"""Models and database functions for airfare project
https://github.com/wordswithchung/hackbright-project."""

from flask_sqlalchemy import SQLAlchemy
import calendar

import os

db = SQLAlchemy()

# MODEL DEFINITIONS ##########

class Airport(db.Model):
    """List of all airport codes with longitude and lattitude info to
    calculate distance. Info from http://openflights.org/data.html

    Airport ID  Unique OpenFlights identifier for this airport.
    Name    Name of airport. May or may not contain the City name.
    City    Main city served by airport. May be spelled differently from Name.
    Country Country or territory where airport is located.
    IATA/FAA    3-letter FAA code, for airports located in Country "United
                States of America".
    3-letter IATA code, for all other airports. Blank if not assigned.
    ICAO    4-letter ICAO code. Blank if not assigned.
    Latitude    Decimal degrees, usually to six significant digits.
                Negative is South, positive is North.
    Longitude   Decimal degrees, usually to six significant digits.
                Negative is West, positive is East.
    Altitude    In feet.
    Timezone    Hours offset from UTC. Fractional hours are expressed as
                decimals, eg. India is 5.5.
    DST Daylight savings time. One of E (Europe), A (US/Canada), S (South
        America), O (Australia), Z (New Zealand), N (None) or U (Unknown).
    Tz database time zone   Timezone in "tz" (Olson) format

    Sample data:
    507,"Heathrow","London","United Kingdom","LHR","EGLL",51.4775,-0.461389,83,
        0,"E","Europe/London"
    26,"Kugaaruk","Pelly Bay","Canada","YBB","CYBB",68.534444,-89.808056,56,-7,
        "A","America/Edmonton"
    """

    __tablename__ = "airports"

    airport_id = db.Column(db.Integer)
    name = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    code = db.Column(db.String(3), primary_key=True)
    icao = db.Column(db.String(4))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    alt = db.Column(db.Integer)
    timezone = db.Column(db.Float)
    dst = db.Column(db.String(1))
    tz = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""
        # must pass in self = self so that it knows
        # dictionary
        return "<Airport code={self.code} city={self.city}>".format(self=self)


class Airfare(db.Model):
    """Historical airfare info. Data web scraped from www.faredetective.com.

    Sample data:
        {"depart": "ZRH", "average_price": "1158", "arrive": "MIA",
        "lowest_price": "1157.53", "cheapest_month": "April"},
    """

    __tablename__ = "airfares"

    airfare_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    depart = db.Column(db.String(3), db.ForeignKey("airports.code"))
    arrive = db.Column(db.String(3), db.ForeignKey("airports.code"))
    lowest_price = db.Column(db.Float)
    average_price = db.Column(db.Float)
    cheapest_month = db.Column(db.String(10))

    aport = db.relationship("Airport", foreign_keys=[arrive],
                                       backref=db.backref("afare",
                                       order_by=average_price))
    dport = db.relationship("Airport", foreign_keys=[depart],
                                       backref=db.backref("dfare",
                                       order_by=average_price))


    @staticmethod
    def choose_locations(month, depart):
        """Figure out which locations to recommend to user based on their
        desired month of travel.

        Sample inputs:
            month = "November"
            depart = Port instance object
        """

        month = calendar.month_name[month] # convert to longform month name

        best_bet = (db.session.query(Airfare).filter(Airfare.depart==depart,
                                Airfare.cheapest_month==month)
                                .join(Airport, Airfare.arrive==Airport.code)
                                .order_by(Airport.city).all())

        if len(best_bet) > 10:
            return best_bet
        else:
            best_bet = (db.session.query(Airfare).filter(Airfare.depart==depart)
                                .join(Airport, Airfare.arrive==Airport.code)
                                .order_by(Airport.city).all())
            return best_bet


    @staticmethod
    def create_map_airfare_objs():
        """Create objects out of the airfares table in the database for JavaScript
        to render from the /map route."""

        airfares = {}

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

        return airfares


    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<depart={self.depart} arrive={self.arrive} "
                "average_price={self.average_price} "
                "cheapest_month={self.cheapest_month}>".format(self=self))


# HELPER ##########

def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///airfare'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
