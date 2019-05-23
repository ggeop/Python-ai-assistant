import sys
import re
import subprocess
import wikipedia
import logging
from pyowm import OWM
from datetime import datetime

from jarvis.settings import WEATHER_API
from jarvis.assistant_utils import assistant_response


class ActionManager:

    @classmethod
    def open_website_in_browser(cls, tag, voice_transcript, action):
        """
        Opens a web page in the browser.
        :param tag: string (e.g 'open')
        :param voice_transcript: string (e.g 'open youtube')

        NOTE: If in the voice_transcript there are more than one commands_dict
        e.g voice_transcript='open youtube and open netflix' the application will find
        and execute only the first one, in our case will open the youtube.
        """
        reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
        if reg_ex:
            domain = reg_ex.group(1)
            assistant_response('Yes sir, I will open the {0}'.format(domain))
            url = cls._create_url(domain)
            subprocess.Popen(["python", "-m",  "webbrowser",  "-t",  url], stdout=subprocess.PIPE)

    @classmethod
    def _create_url(cls, tag):
        """
        Creates a url. It checks if there is .com suffix and add it if it not exist.
        :param tag: string (e.g youtube)
        :return: string (e.g http://www.youtube.com)
        """
        if re.search('.com', tag):
            url = 'http://www.' + tag
        else:
            url = 'http://www.' + tag + '.com'
        return url

    @classmethod
    def tell_the_weather(cls, tag, voice_transcript, action):
        """
        Tells the weather of a place
        :param tag: string (e.g 'weather')
        :param voice_transcript: string (e.g 'weather in London')
        """
        reg_ex = re.search(tag + ' in ([a-zA-Z]+)', voice_transcript)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key=WEATHER_API['key'])
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(WEATHER_API['unit'])
            assistant_response('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum '
                               'temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))

    @staticmethod
    def tell_the_time(**kwargs):
        """
        Tells ths current time
        """
        now = datetime.now()
        assistant_response('Current time is: {0}:{1}'.format(now.hour, now.minute))

    @classmethod
    def tell_me_about(cls, tag, voice_transcript, action):
        """
        Tells about something by searching in wikipedia
        :param tag: string (e.g 'about')
        :param voice_transcript: string (e.g 'about google')
        """
        reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                response = cls._decoded_wiki_response(topic)
                assistant_response(response)
        except Exception as e:
            logging.error(e)

    @classmethod
    def _decoded_wiki_response(cls, topic):
        ny = wikipedia.page(topic)
        data = ny.content[:500].encode('utf-8')
        response = ''
        response += data.decode()
        return response

    @staticmethod
    def enable_jarvis(**kwargs):
        """
        Creates the assistant respond according to the datetime hour and
        updates the execute state.
        """
        now = datetime.now()
        day_time = int(now.strftime('%H'))

        if day_time < 12:
            assistant_response('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            assistant_response('Hello Sir. Good afternoon')
        else:
            assistant_response('Hello Sir. Good evening')
        assistant_response('What do you want to do for you sir?')

        return {'ready_to_execute': True,
                'enable_time': now}

    @staticmethod
    def disable_jarvis(**args):
        assistant_response('Bye bye Sir. Have a nice day')
        logging.debug('Application terminated gracefully.')
        sys.exit()
