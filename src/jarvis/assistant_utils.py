import sys
import traceback
import logging.config
from google_speech import Speech
from jarvis.settings import GOOGLE_SPEECH

from jarvis.settings import GENERAL_SETTINGS

logging.config.fileConfig(fname='config.conf', disable_existing_loggers=False)

# Create logger
logger = logging.getLogger(__name__)


def log(func):
    def wrapper(*args, **kwargs):
        try:
            logger.info(func.__name__)
            func(*args, **kwargs)
        except Exception as e:
            logger.error(func.__name__)
            traceback.print_exc(file=sys.stdout)

    return wrapper


@log
def assistant_response(text):
    if GENERAL_SETTINGS['response_in_speech']:
        speech = Speech(text, GOOGLE_SPEECH['lang'])
        speech.play()
    if GENERAL_SETTINGS['response_in_text']:
        print(text)

