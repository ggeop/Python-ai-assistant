import sys
import re
import os
import psutil
import subprocess
import wikipedia
import logging
import requests
from pyowm import OWM
from datetime import datetime
from bs4 import BeautifulSoup as bs

from jarvis.settings import WEATHER_API
from jarvis.assistant_utils import assistant_response


class SkillManager:

    @staticmethod
    def enable_jarvis(**kwargs):
        """
        Creates the assistant respond according to the datetime hour and
        updates the execute state.
        """
        now = datetime.now()
        day_time = int(now.strftime('%H'))

        if day_time < 12:
            assistant_response('Good morning human')
        elif 12 <= day_time < 18:
            assistant_response('Good afternoon human')
        else:
            assistant_response('Good evening human')
        assistant_response('What do you want to do for you?')

        return {'ready_to_execute': True,
                'enable_time': now}

    @staticmethod
    def disable_jarvis(**kargs):
        """
        Shutdown the assistant service
        :param args:
        :return:
        """
        assistant_response('Bye bye!!')
        logging.debug('Application terminated gracefully.')
        sys.exit()

    @classmethod
    def open_website_in_browser(cls, tag, voice_transcript, skill):
        """
        Opens a web page in the browser.
        :param tag: string (e.g 'open')
        :param voice_transcript: string (e.g 'open youtube')

        NOTE: If in the voice_transcript there are more than one commands_dict
        e.g voice_transcript='open youtube and open netflix' the application will find
        and execute only the first one, in our case will open the youtube.
        """
        reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
        try:
            if reg_ex:
                domain = reg_ex.group(1)
                url = cls._create_url(domain)
                assistant_response('Sure')
                subprocess.Popen(["python", "-m",  "webbrowser",  "-t",  url], stdout=subprocess.PIPE)
                assistant_response('I opened the {0}'.format(domain))
        except Exception as e:
            logging.debug(e)
            assistant_response("I can't find this domain '{0}'".format(domain))

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
    def tell_the_weather(cls, tag, voice_transcript, skill):
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
                    owm = OWM(API_key=WEATHER_API['key'])
                    if owm.is_API_online():
                        obs = owm.weather_at_place(city)
                        w = obs.get_weather()
                        k = w.get_status()
                        x = w.get_temperature(WEATHER_API['unit'])
                        assistant_response('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum '
                                       'temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
                    else:
                        assistant_response("Sorry the weather API is not available now..")
                else:
                    assistant_response("Weather forecast is not working.\n"
                                       "You can get an Weather API key from: https://openweathermap.org/appid")
        except Exception as e:
            logging.debug(e)
            assistant_response("I faced an issue with the weather site..")

    @staticmethod
    def tell_the_time(**kwargs):
        """
        Tells ths current time
        """
        now = datetime.now()
        assistant_response('The current time is: {0}:{1}'.format(now.hour, now.minute))

    @classmethod
    def tell_me_about(cls, tag, voice_transcript, skill):
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
            logging.debug(e)
            assistant_response(" I can't find on the internet what you want")

    @classmethod
    def _decoded_wiki_response(cls, topic):
        """
        A private method for decoding the wiki response.
        :param topic: string
        :return:
        """
        ny = wikipedia.page(topic)
        data = ny.content[:500].encode('utf-8')
        response = ''
        response += data.decode()
        return response

    @classmethod
    def assistant_check(cls, **kargs):
        """
        Responses that assistant can hear the user.
        """
        assistant_response('Yes, I hear you!')

    @classmethod
    def open_libreoffice_calc(cls, **kargs):
        """
        Opens libreoffice calc application
        """
        # TODO: Refactor all libreoffice methods in one
        subprocess.Popen(['libreoffice', '-calc'], stdout=subprocess.PIPE)
        assistant_response('I opened a new calc document..')

    @classmethod
    def open_libreoffice_writer(cls, **kargs):
        """
        Opens libreoffice writer application
        """
        subprocess.Popen(['libreoffice', '-writer'], stdout=subprocess.PIPE)
        assistant_response('I opened a new writer document..')

    @classmethod
    def open_libreoffice_impress(cls, **kargs):
        """
        Opens libreoffice impress application
        """
        subprocess.Popen(['libreoffice', '-impress'], stdout=subprocess.PIPE)
        assistant_response('I opened a new impress document..')

    @staticmethod
    def tell_memory_consumption(**kwargs):
        """
        Responds the memory consumption of the assistant process
        """
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0] / 2. ** 30  # memory use in GB...I think
        assistant_response('I use {} GB..'.format(memoryUse))

    @staticmethod
    def open_in_youtube(tag, voice_transcript, **kwargs):
        """
        Open a video in youtube.
        :param tag: string (e.g 'tdex')
        :param voice_transcript: string (e.g 'open in youtube tdex')
        """
        # TODO:  Replace with YOUTUBE API
        reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
        try:
            if reg_ex:
                search_text = reg_ex.group(1)
                base = "https://www.youtube.com/results?search_query=" + "&orderby=viewCount"
                r = requests.get(base + search_text.replace(' ', '+'))
                page = r.text
                soup = bs(page, 'html.parser')
                vids = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})
                video = 'https://www.youtube.com' + vids[0]['href']
                subprocess.Popen(["python", "-m", "webbrowser", "-t", video], stdout=subprocess.PIPE)
        except Exception as e:
            logging.debug(e)
            assistant_response("I can't find what do you want in Youtube..")

