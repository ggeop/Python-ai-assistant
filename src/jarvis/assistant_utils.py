import sys
import os
import traceback
import logging.config
from google_speech import Speech
from subprocess import call
from jarvis.settings import GOOGLE_SPEECH

from jarvis.settings import GENERAL_SETTINGS


Jarvis_logo = ""\
"         _                  _      \n"\
"        | |                (_)     \n"\
"        | | __ _ _ ____   ___ ___  \n"\
"   _    | |/ _` | '__\ \ / / / __| \n"\
"   | |__| | (_| | |   \ V /| \__ \ \n"\
"    \____/ \__,_|_|    \_/ |_|___/ \n\n"


class OutputStyler:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


logging.config.fileConfig(fname='config.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)  # Create logger


def log(func):
    def wrapper(*args, **kwargs):
        try:
            logger.debug(func.__name__)
            func(*args, **kwargs)
        except Exception as e:
            logger.error(func.__name__)
            traceback.print_exc(file=sys.stdout)

    return wrapper


@log
def assistant_response(text):
    """
    Assistant response in voice or/and in text
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_speech']:
        speech = Speech(text, GOOGLE_SPEECH['lang'])
        speech.play()
    if GENERAL_SETTINGS['response_in_text']:
        response = GENERAL_SETTINGS['assistant_name'] + ': ' + text + '\n'
        sys.stdout.write(OutputStyler.GREEN + response + OutputStyler.ENDC)


def user_speech_playback(text):
    user_speech = str(OutputStyler.GREEN + 'You: ' + text)
    sys.stdout.write(OutputStyler.BLUE + user_speech + OutputStyler.ENDC)


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
    sys.stdout.write(OutputStyler.HEADER + Jarvis_logo + OutputStyler.ENDC)
