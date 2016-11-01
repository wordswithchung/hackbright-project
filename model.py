"""Models and database functions for airfare project
https://github.com/wordswithchung/hackbright-project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# MODEL DEFINITIONS ##########

class Airport(db.Model):
    """List of all airport codes. Data acquired from: https://iatacodes.org/

    Sample data:
    {"code":"ZZV","name":"Zanesville","country_code":"US"}
    """

    __tablename__ = "airports"

    code = db.Column(db.String(3), primary_key=True)
    country_code = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Airport code={} country_code={} name={}>".format(self.code,
                                                           self.country_code,
                                                           self.name,)


class Airfare(db.Model):
    """Historical airfare info. Data web scraped from www.faredetective.com.

    Sample data:

    """

    __tablename__ = "airfares"

    airfare_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    depart = db.Column(db.String(3), db.ForeignKey("airports.code"))
    arrive = db.Column(db.String(3), db.ForeignKey("airports.code"))
    lowest_price = db.Column(db.Float)
    average_price = db.Column(db.Float)
    cheapest_month = db.Column(db.String(10))

    aport = db.relationship("Airport", foreign_keys=[arrive],
                                       backref=db.backref("airfares"))
    dport = db.relationship("Airport", foreign_keys=[depart],
                                       backref=db.backref("fares"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<depart={} arrive={} average_price={} 
                cheapest_month={}>""".format(self.depart,
                                             self.arrive,
                                             self.average_price,
                                             self.cheapest_month,)

# HELPER ##########

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///airfare'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
