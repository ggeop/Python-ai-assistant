# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
import json
import logging

from jarvis.settings import IPSTACK_API
from jarvis.skills.collection.internet import InternetSkills
from jarvis.skills.skill import AssistantSkill


class LocationSkill(AssistantSkill):

    @classmethod
    def get_current_location(cls, **kwargs):
        location_results = cls.get_location()
        if location_results:
            city, latitude, longitude = location_results
            cls.response("You are in {0}".format(city))
    
    @classmethod
    def get_location(cls):
        try:
            send_url = "http://api.ipstack.com/check?access_key=" + IPSTACK_API['key']
            geo_req = requests.get(send_url)
            geo_json = json.loads(geo_req.text)
            latitude = geo_json['latitude']
            longitude = geo_json['longitude']
            city = geo_json['city']
            return city, latitude, longitude
        except Exception as e:
            if InternetSkills.internet_availability():
                # If there is an error but the internet connect is good, then the location API has problem
                cls.console(error_log=e)
                logging.debug("Unable to get current location with error message: {0}".format(e))
                return None
