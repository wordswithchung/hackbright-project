"""ORPHAN CODE"""

from haversine import distance
from model import Airfare, Port, connect_to_db, db
from sqlalchemy import func

def calculate_cost_per_mile(airfare_object):
    """Given one airfare object, calculate the cost per mile."""

    a = Port.query.filter_by(code=airfare_object.arrive).first()
    d = Port.query.filter_by(code=airfare_object.depart).first()

    return airfare_object.average_price / distance([a.lat, a.lon],
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

def calc_cost_per_mile(self):
    """Given one airfare object, calculate the cost per mile."""

    a = Port.query.filter_by(code=self.arrive).first()
    d = Port.query.filter_by(code=self.depart).first()

    return self.average_price / distance([a.lat, a.lon],
                                         [d.lat, d.lon])

# to seed the seed_data/list.txt file
with open('seed_data/list.txt', 'w') as lst:
    for line in h:
        line = line.rstrip()
        lst.write('\"' + line + '\", ')