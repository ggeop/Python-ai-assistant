import sys
import os
import requests
import traceback
import logging
from logging import config
from google_speech import Speech
from subprocess import call
import wolframalpha

from jarvis.settings import GOOGLE_SPEECH, GENERAL_SETTINGS, LOG_SETTINGS
from jarvis.settings import WOLFRAMALPHA_API


jarvis_logo = "\n"\
"      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗\n"\
"      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝\n"\
"      ██║███████║██████╔╝██║   ██║██║███████╗\n"\
" ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║\n"\
" ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║\n"\
"  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝\n"


start_text = "\n"\
" ###############################################\n"\
" #    Jarvis Python Voice Assistant Platform   #\n"\
" ###############################################\n"


class OutputStyler:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    CYAN = '\033[36m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Create a Console & Rotating file logger
config.dictConfig(LOG_SETTINGS)


def log(func):
    """
    Logging wrapper
    :param func: function object
    """
    def wrapper(*args, **kwargs):
        try:
            logging.debug(func.__name__)
            func(*args, **kwargs)
        except Exception as e:
            logging.error(func.__name__)
            traceback.print_exc(file=sys.stdout)
    return wrapper


def assistant_response(text):
    """
    Assistant response in voice or/and in text
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_speech']:
        speech = Speech(text, GOOGLE_SPEECH['lang'])
        speech.play()
    if GENERAL_SETTINGS['response_in_text']:
        assistant_name = GENERAL_SETTINGS['assistant_name'] + ': '
        print('-'*48)
        print(assistant_name + OutputStyler.CYAN + text + OutputStyler.ENDC)
        print('-'*48 + '\n')


def user_speech_playback(text):
    """
    Prints the user commands
    """
    print('-' * 48)
    print('You: ' + OutputStyler.CYAN + text +'\n' + OutputStyler.ENDC)
    print('-'*48 + '\n')


def _clear():
    """
    Clear stdout
    """
    _ = call('clear' if os.name == 'posix' else 'cls')  # check and make call for specific operating system


def start_up():
    """
    Clear the console and print the assistant logo.
    """
    _clear()
    print(OutputStyler.CYAN + jarvis_logo + OutputStyler.ENDC)
    print(OutputStyler.HEADER + start_text + OutputStyler.ENDC)


def call_wolframalpha(voice_transcript):
    """
    Make a request in wolframalpha API and prints the response.
    """
    client = wolframalpha.Client(WOLFRAMALPHA_API['key'])
    try:
        if WOLFRAMALPHA_API['key']:
            res = client.query(voice_transcript)
            assistant_response(next(res.results).text)
            logging.debug('Successful response from Wolframalpha')
        else:
            assistant_response("WolframAlpha API is not working.\n"
                               "You can get an API key from: https://developer.wolframalpha.com/portal/myapps/ ")
    except:
        logging.debug('There is not answer with wolframalpha')
        assistant_response('Sorry, but I can not understand what do you want')


def internet_check(url='http://www.google.com/', timeout=2):
    """
    Internet connectivity check.
    """
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        logging.info("No internet connection.")
        assistant_response("I inform you that I face internet connectivity problem")
    return False