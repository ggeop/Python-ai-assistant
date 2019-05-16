import re
import sys
import subprocess
import wikipedia
import logging
from datetime import datetime

from jarvis.command_words import CommandWords
from jarvis.settings import *
from jarvis.assistant_utils import assistant_response


class ActionController:

    @classmethod
    def wake_up(cls, words):
        if CommandWords.hello in words:
            cls._wake_up_response()
            return True

    @classmethod
    def _wake_up_response(cls):
        now = datetime.now()
        day_time = int(now.strftime('%H'))
        if day_time < 12:
            assistant_response('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            assistant_response('Hello Sir. Good afternoon')
        else:
            assistant_response('Hello Sir. Good evening')

    @classmethod
    def shutdown(cls, words):
        if CommandWords.shutdown in words:
            assistant_response('Bye bye Sir. Have a nice day')
            sys.exit()

    @classmethod
    def open_website_in_browser(cls, words):
        reg_ex = re.search(BROWSER_TRIGGERING_WORD + ' (.+)', words)
        if reg_ex:
            domain = reg_ex.group(1)
            assistant_response('Open the site {0}'.format(domain))
            url = 'http://www.' + domain
            subprocess.Popen(["python", "-m",  "webbrowser",  "-t",  url], stdout=subprocess.PIPE)
        else:
            pass

    @classmethod
    def tell_the_weather(cls, words):
        pass

    @classmethod
    def tell_the_time(cls):
        now = datetime.now()
        assistant_response('Current time is %d hours %d minutes' % (now.hour, now.minute))

    @classmethod
    def tell_me_about(cls, words):
        reg_ex = re.search('tell me about (.*)', words)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                assistant_response(ny.content[:500].encode('utf-8'))
        except Exception as e:
                logging.info(e)
