"""Helper functions that hit the database."""

import math

def calc_distance(airfares):
    """Calculate distance between two airport objects, given a list of
    airfare objects. Slightly modified code from:
    https://gist.github.com/rochacbruno/2883505#file-haversine-py

    Haversine formula example in Python
    Author: Wayne Dyck
    """

    distances = []

    for airfare in airfares:
        lat1, lon1 = airfare.dport.lat, airfare.dport.lng
        lat2, lon2 = airfare.aport.lat, airfare.aport.lng
        radius = 3959 # miles

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c

        distances.append(int(d))

    return distances