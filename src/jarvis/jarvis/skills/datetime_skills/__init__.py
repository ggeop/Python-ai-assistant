from datetime import datetime, date
from jarvis.core.response import assistant_response


def tell_the_time(**kwargs):
    """
    Tells ths current time
    """
    now = datetime.now()
    assistant_response('The current time is: {0}:{1}'.format(now.hour, now.minute))


def tell_the_date(**kwargs):
    """
    Tells ths current date
    """
    today = date.today()
    assistant_response('The current date is: {0}'.format(today))
