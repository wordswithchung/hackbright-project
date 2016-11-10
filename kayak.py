from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def make_kayak_urls(airfares, start, end):
    """Takes airfare objects and generates Kayak URLs.

    Input:
    - airfare objects
    - start date
    - end date
    """

    kayak_urls = []
    for fare in airfares:
        kayak_urls.append("https://www.kayak.com/flights/" + fare.depart +
            "-" + fare.arrive + "/" + start + "/" + end)

    return kayak_urls