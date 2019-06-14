import re
import logging
from pyowm import OWM


from jarvis.settings import WEATHER_API
from jarvis.utils.response_utils import assistant_response


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
    reg_ex = re.search(tag + ' in ([a-zA-Z]+)', voice_transcript)
    try:
        if reg_ex:
            if WEATHER_API['key']:
                city = reg_ex.group(1)
                status, temperature = _get_weather_status_and_temperature(city)
                if status and temperature:
                    assistant_response('Current weather in %s is %s.\n'
                                       'The maximum temperature is %0.2f degree celcius. \n'
                                       'The minimum temperature is %0.2f degree celcius.'
                                       % (city, status, temperature['temp_max'], temperature['temp_min'])
                                       )
                else:
                    assistant_response("Sorry the weather API is not available now..")
            else:
                assistant_response("Weather forecast is not working.\n"
                                   "You can get an Weather API key from: https://openweathermap.org/appid")
    except Exception as e:
        logging.debug(e)
        print(e)
        assistant_response("I faced an issue with the weather site..")
