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

import logging
import sys
import time
from datetime import datetime

from jarvis.skills.assistant_skill import AssistantSkill
from jarvis.utils.startup import play_activation_sound
from jarvis.utils.mongoDB import db
from jarvis.enumerations import InputMode, MongoCollections


class ActivationSkills(AssistantSkill):

    @classmethod
    def enable_assistant(cls, **kwargs):
        """
        Plays activation sound and creates the assistant response according to the day hour.
        """
        input_mode = db.get_documents(collection=MongoCollections.GENERAL_SETTINGS.value)[0]['input_mode']
        if input_mode == InputMode.VOICE.value:
            try:
                play_activation_sound()
            except Exception as e:
                logging.error("Error with the execution of skill with message {0}".format(e))
                cls.response("Sorry I faced an issue")
            time.sleep(1)
        cls.assistant_greeting(kwargs)

    @classmethod
    def disable_assistant(cls, **kwargs):
        """
        - Clear console
        - Shutdown the assistant service
        """
        cls.response('Bye')
        time.sleep(1)
        logging.debug('Application terminated gracefully.')
        sys.exit()

    @classmethod
    def assistant_greeting(cls, *kwargs):
        """
        Assistant greeting based on day hour.
        """
        now = datetime.now()
        day_time = int(now.strftime('%H'))

        if day_time < 12:
            cls.response('Good morning')
        elif 12 <= day_time < 18:
            cls.response('Good afternoon')
        else:
            cls.response('Good evening')
