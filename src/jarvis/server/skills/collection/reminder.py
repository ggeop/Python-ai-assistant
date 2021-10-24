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

import os
import re
import time
import datetime

from threading import Thread
from playsound import playsound
from apscheduler.schedulers.background import BackgroundScheduler

from jarvis.utils.input import validate_digits_input
from jarvis.skills.skill import AssistantSkill
from jarvis.utils.console import OutputStyler

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


class ReminderSkills(AssistantSkill):

    @classmethod
    def _get_reminder_duration_and_time_interval(cls, voice_transcript):
        """
        Extracts the duration and the time interval from the voice transcript.

        NOTE: If there are multiple time intervals, it will extract the first one.
        """
        for time_interval in time_intervals.values():
            for variation in time_interval['variations']:
                if variation in voice_transcript:
                    # Change '[0-9]'to '([0-9])' and now the skill is working
                    reg_ex = re.search('([0-9])', voice_transcript)
                    duration = reg_ex.group(1)
                    return duration, time_interval['scheduler_interval']

    @classmethod
    def create_reminder(cls, voice_transcript, **kwargs):
        """
        Creates a simple reminder for the given time interval (seconds or minutes or hours..)
        :param voice_transcript: string (e.g 'Make a reminder in 10 minutes')
        """
        reminder_duration, scheduler_interval = cls._get_reminder_duration_and_time_interval(voice_transcript)

        def reminder():
            cls.response("Hey, I remind you that now the {0} {1} passed!".format(reminder_duration, scheduler_interval))
            job.remove()

        try:
            if reminder_duration:
                scheduler = BackgroundScheduler()
                interval = {scheduler_interval: int(reminder_duration)}
                job = scheduler.add_job(reminder, 'interval', **interval)
                cls.response("I have created a reminder in {0} {1}".format(reminder_duration, scheduler_interval))
                scheduler.start()

        except Exception as e:
            cls.console(error_log=e)
            cls.response("I can't create a reminder")

    @classmethod
    def set_alarm(cls, voice_transcript, **kwargs):

        # ------------------------------------------------
        # Current Limitations
        # ------------------------------------------------

        # - User can set alarm only for the same day
        # - Works only for specific format hh:mm
        # - Alarm sounds for 12 secs and stops, user can't stop interrupt it.
        #   -- Future improvement is to ring until user stop it.

        cls.response("Yes, I will set an alarm")

        alarm_hour = validate_digits_input(message="Tell me the exact hour", values_range=[0, 24])
        alarm_minutes = validate_digits_input(message="Now tell me the minutes", values_range=[0, 59])

        try:
            thread = Thread(target=cls._alarm_countdown, args=(alarm_hour, alarm_minutes))
            thread.start()
        except Exception as e:
            cls.console(error_log="Failed to play alarm with error message: {0}".format(e))

    @classmethod
    def _alarm_countdown(cls, alarm_hour, alarm_minutes):

        now = datetime.datetime.now()

        alarm_time = datetime.datetime.combine(now.date(), datetime.time(alarm_hour, alarm_minutes, 0))
        waiting_period = alarm_time - now

        if waiting_period < datetime.timedelta(0):
            # Choose 8PM today as the time the alarm fires.
            # This won't work well if it's after 8PM, though.
            cls.response('This time has past for today')
        else:
            # Successful setup message
            response_message = "Alarm - {0}:{1} for today is configured " \
                               + OutputStyler.GREEN + "successfully!" + OutputStyler.ENDC
            cls.response(response_message.format(alarm_hour, alarm_minutes))

            # Alarm countdown starts
            time.sleep((alarm_time - now).total_seconds())
            cls.response("Wake up! It's {0}".format(datetime.datetime.now().strftime('%H:%M')))

            skills_dir = os.path.dirname(__file__)
            alarm_soundfile = os.path.join(skills_dir, '..', 'files', 'analog_watch_alarm.wav')

            playsound(alarm_soundfile)
