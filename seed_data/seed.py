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
    f = open("seed_data/ports.csv")
    ports = []
    for line in f:
        ports.append(line[:3])
    print ports

    dictionary = json.load(jf)
    for i, item in enumerate(dictionary):
        print "item['depart'].encode('ascii', 'ignore') ", item['depart'].encode('ascii', 'ignore')
        if (item['depart'].encode('ascii', 'ignore') in ports) or (item['arrive'
            ].encode('ascii', 'ignore') in ports):
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
    f = open("seed_data/airports.csv")
    for line in f:
        l = line.rstrip().split(',')
        (airport_id, name, city, country, code, icao, lat, lng,
            alt, timezone, dst, tz) = l
        airport = Airport(airport_id=airport_id,
                          name=name,
                          city=city,
                          country=country,
                          code=code,
                          icao=icao,
                          lat=lat,
                          lng=lng,
                          alt=alt,
                          timezone=timezone,
                          dst=dst,
                          tz=tz,)

        db.session.add(airport)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_airports()
    load_airfares()
    print "All's well that ends in the database well."
