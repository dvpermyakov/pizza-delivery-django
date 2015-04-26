import requests
from datetime import datetime

__author__ = 'dvpermyakov'

API_KEY = 'AIzaSyDbvqxffzEt4BTNKImswtk1zqn77uXFGxA'


def get_timezone(address):
    url = 'https://maps.googleapis.com/maps/api/timezone/json'
    params = {
        'key': API_KEY,
        'location': '%s,%s' % (address.lat, address.lon),
        'timestamp': (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.get(url, params=params, headers=headers).json()
    return response