from datetime import datetime
from jarvis.utils.response_utils import assistant_response


def tell_the_time(**kwargs):
    """
    Tells ths current time
    """
    now = datetime.now()
    assistant_response('The current time is: {0}:{1}'.format(now.hour, now.minute))