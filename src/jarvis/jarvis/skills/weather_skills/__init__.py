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

import re
import logging
import time

from pyowm import OWM

from jarvis.settings import WEATHER_API
from jarvis.skills.location_skill import get_location


def _get_weather_status_and_temperature(city):
    owm = OWM(API_key=WEATHER_API['key'])
    if owm.is_API_online():
        obs = owm.weather_at_place(city)
        weather = obs.get_weather()
        status = weather.get_status()
        temperature = weather.get_temperature(WEATHER_API['unit'])
        return status, temperature
    else:
        return None, None


def tell_the_weather(tag, voice_transcript, **kwargs):
    """
    Tells the weather of a place
    :param tag: string (e.g 'weather')
    :param voice_transcript: string (e.g 'weather in London')
    """
    reg_ex = re.search(tag + ' [a-zA-Z][a-zA-Z] ([a-zA-Z]+)', voice_transcript)
    try:
        if WEATHER_API['key']:
            city = _get_city(reg_ex)
            status, temperature = _get_weather_status_and_temperature(city)
            if status and temperature:
                print('Current weather in %s is %s.\n'
                                   'The maximum temperature is %0.2f degree celcius. \n'
                                   'The minimum temperature is %0.2f degree celcius.'
                                   % (city, status, temperature['temp_max'], temperature['temp_min'])
                                   )
            else:
                print("Sorry the weather API is not available now..")
        else:
            print("Weather forecast is not working.\n"
                               "You can get an Weather API key from: https://openweathermap.org/appid")

    except Exception as e:
        logging.debug(e)
        print("I faced an issue with the weather site..")


def _get_city(reg_ex):
    if not reg_ex:
        city, latitude, longitude = get_location()
        print("You are in {0}".format(city))
        time.sleep(1)
    else:
        city = reg_ex.group(1)
    return city
