"""Utility file to seed airfare database from iatacodes.org and
faredectective.com stored in seed_data/"""

import json
from sqlalchemy import func
from server import app


def load_airports():
    """Load airports -- code, name, country code -- from seed_data/airports.json
     into database."""

    print "Airports"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate airports.
    Airport.query.delete()

    # Open airports.json file and parse data into airport table
    jf = open("seed_data/airports.json")
    dictionary = json.load(jf)
    for item in dictionary['response']:
        airport = Airport(code=item['code'],
                          country_code=item['country_code'],
                          name=item['name'],)
    
        db.session.add(airport)

    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()
    
    load_airports()
    load_airfares()
