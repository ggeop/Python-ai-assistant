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

from datetime import datetime, timedelta

from jarvis.core.memory import State
from jarvis.settings import GENERAL_SETTINGS
from jarvis.utils.application_utils import log
from jarvis.skills.skills_registry import BASIC_SKILLS, CONTROL_SKILLS
from jarvis.setup import stt_engine
from jarvis.core.analyzer import Analyzer


class Controller:
    def __init__(self):
        self.to_execute = []
        self.latest_voice_transcript = ''
        self.execute_state = {'ready_to_execute': False, 'enable_time': None}
        #TODO: add stt_engine in processor initilization
        self.stt_engine = stt_engine

    def wake_up_check(self):
        """
        Checks if the state of the skill manager (ready_to_execute)
        and if is not enabled search for enable word in user recorded speech.
        :return: boolean
        """
        if GENERAL_SETTINGS['user_voice_input']:
            if not self.execute_state['ready_to_execute']:
                return self._ready_to_start()
            return self._continue_listening()
        return True

    @log
    def shutdown_check(self):
        """
        Checks if there is the shutdown word, and if exists the assistant service stops.
        """
        transcript_words = self.latest_voice_transcript.split()
        shutdown_tag = set(transcript_words).intersection(CONTROL_SKILLS['disable_assistant']['tags'])

        if bool(shutdown_tag):
            CONTROL_SKILLS['disable_assistant']['skill']()

    def get_transcript(self):
        """
        Capture the words from the recorded audio (audio stream --> free text).
        """
        if GENERAL_SETTINGS['user_voice_input']:
            self.latest_voice_transcript = self.stt_engine.recognize_voice()
        else:
            self.latest_voice_transcript = self.stt_engine.recognize_text()

    def _ready_to_start(self):
        """
        Checks for enable tag and if exists return a boolean
        return: boolean
        """
        self.get_transcript()

        transcript_words = self.latest_voice_transcript.split()
        enable_tag = set(transcript_words).intersection(CONTROL_SKILLS['enable_assistant']['tags'])

        if bool(enable_tag):
            self.execute_state = CONTROL_SKILLS['enable_assistant']['skill']()
            return True

    def _continue_listening(self):
        """
        Checks if the assistant enable time (triggering time + enable period) has passed.
        return: boolean
        """
        if datetime.now() > self.execute_state['enable_time'] + timedelta(seconds=GENERAL_SETTINGS['enable_period']):
            self.execute_state = {'ready_to_execute': False,
                                  'enable_time': None}

            State.is_assistant_enabled = False
            return False

        State.is_assistant_enabled = True
        return True



    @log
    def get_skills(self):
        """
        This method identifies the active skills from the voice transcript
        and updates the skills state.
        e.x. latest_voice_transcript='open youtube'
        Then, the to_execute will be the following:
        to_execute={voice_transcript': 'open youtube',
                             'tag': 'open',
                             'skill': Skills.open_website_in_browser
                    }
        """
        skill = self.analyzer.extract(self.latest_voice_transcript)
        self.to_execute = {'voice_transcript': self.latest_voice_transcript,
                           'skill': skill['skill']}
        logging.debug('to_execute : {0}'.format(self.to_execute))

    def execute(self):
        """
        Execute the user skill and empty skill for execution.
        """
        try:
            if self.to_execute:
                resp = language_processing.create_positive_response(self.latest_voice_transcript)
                TTSEngine.assistant_response(resp)
                logging.debug('Execute skill {0}'.format(self.to_execute.keys()))
                self.to_execute['skill'](**self.to_execute)
            else:
                resp = language_processing.create_negative_response(self.latest_voice_transcript)
                TTSEngine.assistant_response(resp)
                # If there is not an action the assistant make a request in WolframAlpha API
                call_wolframalpha(self.latest_voice_transcript)
        except Exception as e:
            print(e)
            logging.debug("Error with the execution of skill {0} with message {1}".format(self.to_execute.keys(), e))
        # Clear the skills queue
        self.to_execute = {}

