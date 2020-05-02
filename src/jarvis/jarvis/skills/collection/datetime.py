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

from datetime import datetime, date
from jarvis.skills.skill import AssistantSkill

hour_mapping = {'0': 'twelve',
                '1': 'one',
                '2': 'two',
                '3': 'three',
                '4': 'four',
                '5': 'five',
                '6': 'six',
                '7': 'seven',
                '8': 'eight',
                '9': 'nine',
                '10': 'ten',
                '11': 'eleven',
                '12': 'twelve',

                }


class DatetimeSkills(AssistantSkill):

    @classmethod
    def tell_the_time(cls, **kwargs):
        """
        Tells ths current time
        """

        now = datetime.now()
        hour, minute = now.hour, now.minute
        converted_time = cls._time_in_text(hour, minute)
        cls.response('The current time is: {0}'.format(converted_time))

    @classmethod
    def tell_the_date(cls, **kwargs):
        """
        Tells ths current date
        """

        today = date.today()
        cls.response('The current date is: {0}'.format(today))

    @classmethod
    def _get_12_hour_period(cls, hour):
        return 'pm' if 12 <= hour < 24 else 'am'

    @classmethod
    def _convert_12_hour_format(cls, hour):
        return hour - 12 if 12 < hour <= 24 else hour

    @classmethod
    def _create_hour_period(cls, hour):
        hour_12h_format = cls._convert_12_hour_format(hour)
        period = cls._get_12_hour_period(hour)
        return hour_mapping[str(hour_12h_format)] + ' ' + '(' + period + ')'

    @classmethod
    def _time_in_text(cls, hour, minute):

        if minute == 0:
            time = cls._create_hour_period(hour) + " o'clock"
        elif minute == 15:
            time = "quarter past " + cls._create_hour_period(hour)
        elif minute == 30:
            time = "half past " + cls._create_hour_period(hour)
        elif minute == 45:
            hour_12h_format = cls._convert_12_hour_format(hour + 1)
            period = cls._get_12_hour_period(hour)
            time = "quarter to " + hour_mapping[str(hour_12h_format)] + ' ' + '(' + period + ')'
        elif 0 < minute < 30:
            time = str(minute) + " minutes past " + cls._create_hour_period(hour)
        else:
            hour_12h_format = cls._convert_12_hour_format(hour + 1)
            period = cls._get_12_hour_period(hour)
            time = str(60 - minute) + " minutes to " + hour_mapping[str(hour_12h_format)] + ' ' + '(' + period + ')'

        return time
