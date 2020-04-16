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
import speech_recognition as sr

from datetime import datetime, timedelta

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from jarvis.skills.skill_analyzer import SkillAnalyzer
from jarvis.skills.skills_registry import skill_objects, db
from jarvis.core.nlp_processor import ResponseCreator
from jarvis.settings import DEFAULT_GENERAL_SETTINGS
from jarvis.enumerations import InputMode

import jarvis.engines as engines


class Processor:
    def __init__(self, settings_):
        self.settings = settings_
        self.db = db
        self.input_engine = engines.STTEngine(
                                        pause_threshold=self.settings.SPEECH_RECOGNITION.get('pause_threshold'),
                                        energy_theshold=self.settings.SPEECH_RECOGNITION.get('energy_threshold'),
                                        ambient_duration=self.settings.SPEECH_RECOGNITION.get('ambient_duration'),
                                        dynamic_energy_threshold=self.settings.SPEECH_RECOGNITION.get(
                                            'dynamic_energy_threshold'),
                                        sr=sr
                                        ) if self.settings.DEFAULT_GENERAL_SETTINGS.get('input_mode') == InputMode.VOICE.value \
            else engines.TTTEngine()

        self.output_engine = engines.TTSEngine() if self.settings.DEFAULT_GENERAL_SETTINGS.get('response_in_speech') \
            else engines.TTTEngine()
        self.response_creator = ResponseCreator()
        self.skill_analyzer = SkillAnalyzer(
                                            weight_measure=TfidfVectorizer,
                                            similarity_measure=cosine_similarity,
                                            args=self.settings.SKILL_ANALYZER.get('args'),
                                            sensitivity=self.settings.SKILL_ANALYZER.get('sensitivity'),
                                            db=self.db
                                            )

    def run(self):
        """
        This method is the assistant starting point.

        - STEP 1: Waiting for enable keyword (ONLY in 'voice' mode)
        - STEP 2: Retrieve input (voice or text)
        - STEP 3: Matches the input with a skill
        - STEP 4: Create a response
        - STEP 5: Execute matched skill
        - STEP 6: Insert user transcript and response in history collection (in MongoDB)

        """

        # STEP 1
        self._trapped_until_assistant_is_enabled()

        # STEP 2
        transcript = self.input_engine.recognize_input()

        # STEP 3
        skill_to_execute = self._extract_skill(transcript)

        # STEP 4
        response = self.response_creator.create_positive_response(transcript) if skill_to_execute \
            else self.response_creator.create_negative_response(transcript)
        self.output_engine.assistant_response(response)

        # STEP 5
        self._execute_skill(skill_to_execute)

        # STEP 6
        record = {'user_transcript': transcript,
                  'response': response if response else '--',
                  'executed_skill': skill_to_execute if skill_to_execute else '--'
        }
        self.db.insert_many_documents('history', [record])

    def _trapped_until_assistant_is_enabled(self):
        """
        In voice mode assistant waiting to hear an enable keyword to start, until then is trapped in a loop.
        """
        if self.settings.DEFAULT_GENERAL_SETTINGS.get('input_mode') == InputMode.VOICE.value:
            while not ExecutionState.is_ready_to_execute():
                voice_transcript = self.input_engine.recognize_input()
                transcript_words = voice_transcript.split()
                enable_skills = self.db.get_documents('control_skills', {'name': 'enable_assistant'})
                enable_tags = [skill.get('tags') for skill in enable_skills]
                enable_tag = set(transcript_words).intersection(enable_tags)

                if bool(enable_tag):
                    skill_name = self.db.get_documents('control_skills', {'name': 'enable_assistant'}).get('skills')
                    skill_object = skill_objects[skill_name]
                    skill_object()
                    ExecutionState.update()

    def _extract_skill(self, transcript):
        skill = self.skill_analyzer.extract(transcript)
        if skill:
            return {'voice_transcript': transcript, 'skill': skill}

    @staticmethod
    def _execute_skill(skill):
        if skill:
            try:
                logging.debug('Executing skill {0}'.format(skill.get('skill').get('name')))
                skill_func_name = skill.get('skill').get('func')
                skill_func = skill_objects[skill_func_name]
                skill_func(**skill)
            except Exception as e:
                logging.debug("Error with the execution of skill with message {0}".format(e))


class ExecutionState:
    is_enabled = False
    enabled_time = None

    @classmethod
    def reset(cls):
        cls.is_enabled = False
        cls.enable_time = None

    @classmethod
    def update(cls):
        cls.is_enabled = True
        cls.enable_time = datetime.now()

    @classmethod
    def is_ready_to_execute(cls):
        if cls.enabled_time:
            enabled_period_has_passed = datetime.now() > cls.enabled_time + timedelta(seconds=DEFAULT_GENERAL_SETTINGS.get(
                'enabled_period'))
            return enabled_period_has_passed
        else:
            return cls.is_enabled

