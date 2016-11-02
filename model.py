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

    def calc_cost_per_mile(self):
        """Given one airfare object, calculate the cost per mile."""

        a = Port.query.filter_by(code=self.arrive).first()
        d = Port.query.filter_by(code=self.depart).first()

        return self.average_price / distance([a.lat, a.lon],
                                             [d.lat, d.lon])

    @staticmethod
    def calc_cheapest_month(month, depart):
        """Figure out which locations to recommend to user based on their
        desired month of travel.

        Sample inputs:
            month = "April"
            depart = Port instance object
        """

        lst = Airfare.query.filter_by(cheapest_month=month).all()

        # bucketing distances to diversify recommendations
        short_distance = set() # 0 - 999 miles; 10%
        medium_distance = set() # 1,000 - 4,999 miles; 60%
        long_distance = set() # <= 5,000 miles; 30%

        if lst:
            for item in lst:
                arrive = Port.query.filter_by(code=item.arrive).first()
                a = distance([depart.lat, depart.lon],
                             [arrive.lat, arrive.lon])
                if 1 < a <= 999:
                    short_distance.add(arrive.code.encode('ascii', 'ignore'))
                elif 1000 <= a <= 4999:
                    medium_distance.add(arrive.code.encode('ascii', 'ignore'))
                elif a >= 5000:
                    long_distance.add(arrive.code.encode('ascii', 'ignore'))

        return sample(short_distance, 1) + sample(medium_distance, 6) + sample(long_distance, 3)


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
