import sys
import logging
from datetime import datetime


from jarvis.utils.response_utils import assistant_response


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


def disable_jarvis(**kargs):
    """
    Shutdown the assistant service
    :param args:
    :return:
    """
    assistant_response('Bye bye!!')
    logging.debug('Application terminated gracefully.')
    sys.exit()