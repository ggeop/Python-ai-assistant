# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import logging

from apscheduler.schedulers.background import BackgroundScheduler




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
        print("Hey, I remind you that now the {0} {1} passed!"
                           .format(reminder_duration, scheduler_interval))
        job.remove()

    try:
        if reminder_duration:
            scheduler = BackgroundScheduler()
            interval = {scheduler_interval: int(reminder_duration)}
            job = scheduler.add_job(reminder, 'interval', **interval)
            print("I have created a reminder in {0} {1}".format(reminder_duration, scheduler_interval))
            scheduler.start()

    except Exception as e:
        logging.debug(e)
        print("I can't create a reminder")
