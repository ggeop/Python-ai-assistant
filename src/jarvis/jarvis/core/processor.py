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

import speech_recognition as sr
import logging

from enum import Enum
from datetime import datetime, timedelta


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from jarvis.skills.skills_registry import CONTROL_SKILLS, SKILLS
from jarvis.skills.skill_analyzer import SkillAnalyzer
from jarvis.engines.stt import STTEngine
from jarvis.engines.tts import TTSEngine
from jarvis.engines.ttt import TTTEngine
from jarvis.core.nlp_processor import ResponseCreator
from jarvis.settings import GENERAL_SETTINGS


class Processor:
    def __init__(self, settings_):
        self.settings = settings_
        self.input_engine = STTEngine(
                                        pause_threshold=self.settings.SPEECH_RECOGNITION.get('pause_threshold'),
                                        energy_theshold=self.settings.SPEECH_RECOGNITION.get('energy_threshold'),
                                        ambient_duration=self.settings.SPEECH_RECOGNITION.get('ambient_duration'),
                                        dynamic_energy_threshold=self.settings.SPEECH_RECOGNITION.get('dynamic_energy_threshold'),
                                        sr=sr
                                        ) if self.settings.GENERAL_SETTINGS.get('input_mode') == InputMode.VOICE.value else TTTEngine()

        self.output_engine = TTSEngine() if self.settings.GENERAL_SETTINGS.get('response_in_speech') else TTTEngine()

        self.response_creator = ResponseCreator()

        self.skill_analyzer = SkillAnalyzer(
                                            weight_measure=TfidfVectorizer,
                                            similarity_measure=cosine_similarity,
                                            args=self.settings.SKILL_ANALYZER.get('args'),
                                            skills_=SKILLS,
                                            sensitivity=self.settings.SKILL_ANALYZER.get('sensitivity')
                                            )

    def run(self):

        self._trapped_until_assistant_is_enabled()

        transcript = self.input_engine.recognize_input()
        skill_to_execute = self._extract_skill(transcript)
        response = self.response_creator.create_positive_response(transcript) if skill_to_execute \
            else self.response_creator.create_negative_response(transcript)

        self.output_engine.assistant_response(response)
        self._execute_skill(skill_to_execute)

    def _execute_skill(self, skill):
        if skill:
            try:
                skill_method = skill.get('skill').get('skill')
                logging.debug('Executing skill {0}'.format(skill))
                skill_method(**skill)
            except Exception as e:
                logging.debug("Error with the execution of skill with message {0}".format(e))

    def _trapped_until_assistant_is_enabled(self):
        if self.settings.GENERAL_SETTINGS.get('input_mode') == InputMode.VOICE.value:
            while not ExecutionState.is_ready_to_execute():
                voice_transcript = self.input_engine.recognize_input()
                transcript_words = voice_transcript.split()
                enable_tag = set(transcript_words).intersection(CONTROL_SKILLS.get('enable_assistant').get('tags'))

                if bool(enable_tag):
                    CONTROL_SKILLS.get('enable_assistant').get('skill')()
                    ExecutionState.update()

    def _extract_skill(self, transcript):
        skill = self.skill_analyzer.extract(transcript)
        if skill:
            return {'voice_transcript': transcript, 'skill': skill}


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
            enabled_period_has_passed = datetime.now() > cls.enabled_time + timedelta(seconds=GENERAL_SETTINGS.get('enabled_period'))
            return enabled_period_has_passed
        else:
            return cls.is_enabled


class InputMode(Enum):
    VOICE = 'voice'
    TEXT = 'text'
