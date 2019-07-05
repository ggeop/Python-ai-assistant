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

import sys
import time
import logging

from datetime import datetime

from jarvis.utils.application_utils import play_activation_sound, clear
from jarvis.skills.skill_manager import AssistantSkill


class ActivationSkills(AssistantSkill):

    @classmethod
    def enable_assistant(cls, **kwargs):
        """
        Creates the assistant respond according to the datetime hour and
        updates the execute state.
        """
        play_activation_sound()

        now = datetime.now()
        day_time = int(now.strftime('%H'))

        if AssistantSkill.first_activation:
            if day_time < 12:
                cls.response('Good morning human')
                time.sleep(2)
            elif 12 <= day_time < 18:
                cls.response('Good afternoon human')
                time.sleep(2)
            else:
                cls.response('Good evening human')
                time.sleep(2)
            cls.response('What do you want?')
            AssistantSkill.first_activation = False

        return {'ready_to_execute': True,
                'enable_time': now}

    @classmethod
    def disable_assistant(cls, **kargs):
        """
        Shutdown the assistant service
        :param args:
        :return:
        """
        cls.response('Bye')
        time.sleep(1)
        clear()
        logging.debug('Application terminated gracefully.')
        sys.exit()
