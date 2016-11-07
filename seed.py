"""Utility file to seed airfare database from iatacodes.org and
faredectective.com stored in seed_data/"""

import json
from model import Airfare, Airport, connect_to_db, db
from server import app
from sqlalchemy import func


def load_airfares():
    """Load historical airfare info from seed_data/airfare.json file."""

    print "Airfare"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate airports.
    Airfare.query.delete()

    # Open airports.json file and parse data into airport table
    jf = open("seed_data/airfare.json")
    f = open("seed_data/clean_airports.txt")
    ports = []
    for line in f:
        l = line.rstrip().split('|')
        if l[4]:
          ports.append(l[4])
    print ports

    dictionary = json.load(jf)
    for i, item in enumerate(dictionary):
        # print "item['depart'].encode('ascii', 'ignore') ", item['depart'].encode('ascii', 'ignore')
        if (item['depart'].encode('ascii', 'ignore') in ports) or (item['arrive'].encode('ascii', 'ignore') in ports):
            airfare = Airfare(depart=item['depart'],
                          arrive=item['arrive'],
                          lowest_price=float(item['lowest_price'].encode('ascii', 'ignore')),
                          average_price=float(item['average_price'].encode('ascii', 'ignore')),
                          cheapest_month=item['cheapest_month'],)

            db.session.add(airfare)
        else:
            pass

        if i % 100 == 0:
            db.session.commit()

    db.session.commit()

def load_airports():
    """Load airports -- code, name, long, lat -- into database."""

    print "Airports"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate airports.
    Airport.query.delete()

    # Open airports.json file and parse data into airport table
    f = open("seed_data/clean_airports.txt")
    for line in f:
        l = line.rstrip().split('|')
        if l[4]:
            airport = Airport(airport_id=l[0],
                              name=l[1],
                              city=l[2],
                              country=l[3],
                              code=l[4],
                              icao=l[5],
                              lat=l[6],
                              lng=l[7],
                              alt=l[8],
                              timezone=l[9],
                              dst=l[10],
                              tz=l[11],)

        db.session.merge(airport)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_airports()
    load_airfares()
    print "All's well that ends in the database well."
