import requests
import json
import logging

from jarvis.settings import IPSTACK_API
from jarvis.core.response import assistant_response


def get_current_location(**kwargs):
    location_results = get_location()
    if location_results:
        city, latitude, longitude = location_results
        assistant_response('You are in {0}'.format(city))


def get_location():
    try:
        send_url = "http://api.ipstack.com/check?access_key=" + IPSTACK_API['key']
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        latitude = geo_json['latitude']
        longitude = geo_json['longitude']
        city = geo_json['city']
        return city, latitude, longitude
    except Exception as e:
        logging.debug("Unable to get current location with error message: {0}".format(e))
        return None
