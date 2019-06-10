import re
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from jarvis.utils.response_utils import assistant_response


def _get_reminder_duration_and_time_interval(voice_transcript):
    """
    Extracts the duration and the time interval from the voice transcript.

    NOTE:
        If there are multiple time intervals, it will extract the first one.
    """
    time_intervals = {
        'seconds': {'variations': ['sec', 'second', 'seconds'],
                    'scheduler_interval': 'seconds'
                    },
        'minutes': {'variations': ['minute', 'minutes'],
                    'scheduler_interval': 'minutes'
                    },
        'hours': {'variations': ['hour', 'hours'],
                  'scheduler_interval': 'hours'
                  },
        'months': {'variations': ['month', 'months'],
                   'scheduler_interval': 'months'
                   },
        'years': {'variations': ['year', 'years'],
                  'scheduler_interval': 'years'
                  },
    }

    for time_interval in time_intervals.values():
        for variation in time_interval['variations']:
            if variation in voice_transcript:
                print(variation, voice_transcript)
                reg_ex = re.search('[0-9]', voice_transcript)
                duration = reg_ex.group(1)
                return duration, time_interval['scheduler_interval']


def create_reminder(voice_transcript, **kwargs):
    """
    Creates a simple reminder for the given time interval (seconds or minutes or hours..)
    :param voice_transcript: string (e.g 'Make a reminder in 10 minutes')
    """
    reminder_duration, scheduler_interval = _get_reminder_duration_and_time_interval(voice_transcript)

    def reminder():
        assistant_response("Hey, I remind you that now the {0} {1} passed!"
                           .format(reminder_duration, scheduler_interval))
        job.remove()

    try:
        if reminder_duration:
            scheduler = BackgroundScheduler()
            interval = {scheduler_interval: int(reminder_duration)}
            job = scheduler.add_job(reminder, 'interval', **interval)
            assistant_response("I have created a reminder in {0} {1}".format(reminder_duration, scheduler_interval))
            scheduler.start()

    except Exception as e:
        logging.debug(e)
        assistant_response("I can't create a reminder")
