import sys
import traceback
import logging.config
from google_speech import Speech

from jarvis.settings import GOOGLE_SPEECH

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


class CommandWords:
    hello = 'hello'
    shutdown = 'shut down'


@log
def assistant_response(text):
    logging.info('User said: {0}'.format(text))
    speech = Speech(text, GOOGLE_SPEECH['lang'])
    speech.play()

