import logging
import wolframalpha

from jarvis.utils.response_utils import assistant_response
from jarvis.settings import WOLFRAMALPHA_API


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