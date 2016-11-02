"""Models and database functions for airfare project
https://github.com/wordswithchung/hackbright-project."""

from flask_sqlalchemy import SQLAlchemy
from haversine import distance

db = SQLAlchemy()

# MODEL DEFINITIONS ##########

# class Airport(db.Model):
#     """List of all airport codes. Data acquired from: https://iatacodes.org/

#     Sample data:
#         {"code":"ZZV","name":"Zanesville","country_code":"US"}
#     """

#     __tablename__ = "airports"

#     code = db.Column(db.String(3), primary_key=True)
#     country_code = db.Column(db.String(2), nullable=False)
#     name = db.Column(db.String(64), nullable=False)

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Airport code={} country_code={} name={}>".format(self.code,
#                                                            self.country_code,
#                                                            self.name,)

class Port(db.Model):
    """List of all airport codes with longitude and lattitude info to
    calculate distance. Info from https://datahub.io/dataset/global-airports

    Sample data:
        
    """

    __tablename__ = "ports"

    code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Port code={} name={}>".format(self.code, self.name,)


class Airfare(db.Model):
    """Historical airfare info. Data web scraped from www.faredetective.com.

    Sample data:
        {"depart": "ZRH", "average_price": "1158", "arrive": "MIA", 
        "lowest_price": "1157.53", "cheapest_month": "April"},
    """

    __tablename__ = "airfares"

    airfare_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    depart = db.Column(db.String(3), db.ForeignKey("ports.code"))
    arrive = db.Column(db.String(3), db.ForeignKey("ports.code"))
    lowest_price = db.Column(db.Float)
    average_price = db.Column(db.Float)
    cheapest_month = db.Column(db.String(10))

    aport = db.relationship("Port", foreign_keys=[arrive],
                                       backref=db.backref("afare",
                                       order_by=average_price))
    dport = db.relationship("Port", foreign_keys=[depart],
                                       backref=db.backref("dfare",
                                       order_by=average_price))

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
