"""Using requests and BeautifulSoup to get the airfare cost for specific
trips from Kayak.com.

Got info from http://bit.ly/2f6Hkvg

IMPORTANT NOTE (NOVEMBER 4, 2016):
Bailing on this since it's not possible to scrape data from Kayak. :(
"""

from bs4 import BeautifulSoup
import requests


def extract_fare_from_kayak(depart, arrive, start_date, end_date):
    
    kayak = ("https://www.kayak.com/flights/" + depart + "-" + arrive 
             + "/" + start_date + "/" + end_date)
    r = requests.get(kayak)
    soup = BeautifulSoup(r.text, 'html.parser').get_text()

    # http://stackoverflow.com/a/17613662
    price = soup.find_all('span', attrs={'class':'price'}, limit=1)
