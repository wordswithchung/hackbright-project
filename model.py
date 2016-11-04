"""Models and database functions for airfare project
https://github.com/wordswithchung/hackbright-project."""

from flask_sqlalchemy import SQLAlchemy
from haversine import distance
from random import sample

db = SQLAlchemy()

# MODEL DEFINITIONS ##########

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

    @staticmethod
    def locations(month, depart):
        """Figure out which locations to recommend to user based on their
        desired month of travel.

        Sample inputs:
            month = "November"
            depart = Port instance object
        """

        # find all airfare available for depart
        lst = Airfare.query.filter_by(depart=depart.code).all()
        best_bet = [] # locations whose cheapest_month = user's month of travel

        if lst: 
            for item in lst:
                if item.cheapest_month == month:
                    best_bet.append(item)

        if best_bet:
            return best_bet
        else:
            return lst


    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<depart={} arrive={} 
               average_price={} cheapest_month={}>""".format(self.depart,
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
