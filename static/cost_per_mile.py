

from haversine import distance
from model import Airfare, Port, connect_to_db, db
from sqlalchemy import func

def calculate_cost_per_mile(airfare_object):
    """Given one airfare object, calculate the cost per mile."""

    a = Port.query.filter_by(code=airfare_object.arrive).first()
    d = Port.query.filter_by(code=airfare_object.depart).first()

    return airfare_object.average_price / distance([a.lat, a.lon],
                                                   [d.lat, d.lon])
