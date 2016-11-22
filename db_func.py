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

def create_search_result_obj(airfares, distances, kayak_urls):
    """Creates objects out of the search results for JavaScript to render on
    the /search route."""

    data = zip(airfares, distances, kayak_urls)

    info = []
    for airfare, distance, kayak_url in data:
        info.append({
            'arrival_city'  : airfare.aport.city,
            'avg_price'     : int(airfare.average_price),
            'airport_code'  : airfare.arrive,
            'distance'      : distance,
            'kayak_url'     : kayak_url
        })

    return info

