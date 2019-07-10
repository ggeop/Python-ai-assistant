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
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from jarvis.core.controller import SkillController
from jarvis.utils.startup_utils import start_up
from jarvis.settings import GENERAL_SETTINGS, ANALYZER, ROOT_LOG_CONF
from jarvis.skills.skills_registry import CONTROL_SKILLS, SKILLS
from jarvis.skills.skill_analyzer import SkillAnalyzer
from jarvis.settings import SPEECH_RECOGNITION
from jarvis.engines.stt import STTEngine
from jarvis.engines.tts import TTSEngine
from jarvis.engines.ttt import TTTEngine
from jarvis.core.nlp_processor import ResponseCreator
from jarvis.core.console_manager import ConsoleManager


class Processor:
    def __init__(self):
        self.input_engine = STTEngine(
                                        pause_threshold=SPEECH_RECOGNITION['pause_threshold'],
                                        energy_theshold=SPEECH_RECOGNITION['energy_threshold'],
                                        ambient_duration=SPEECH_RECOGNITION['ambient_duration'],
                                        dynamic_energy_threshold=SPEECH_RECOGNITION['dynamic_energy_threshold'],
                                        sr=sr
                                        ) if GENERAL_SETTINGS['user_voice_input'] else TTTEngine()

        self.console_manager = ConsoleManager(
                                              log_settings=ROOT_LOG_CONF,
                                             )
        self.output_engine = TTSEngine(
                                        console_manager=self.console_manager,
                                        speech_response_enabled=GENERAL_SETTINGS['response_in_speech']
                                       )
        self.response_creator = ResponseCreator()

        self.skill_analyzer = SkillAnalyzer(
                                            weight_measure=TfidfVectorizer,
                                            similarity_measure=cosine_similarity,
                                            args=ANALYZER['args'],
                                            skills_=SKILLS,
                                            sensitivity=ANALYZER['sensitivity']
                                            )

        self.skill_controller = SkillController(
                                                settings_=GENERAL_SETTINGS,
                                                input_engine=self.input_engine,
                                                analyzer=self.skill_analyzer,
                                                control_skills=CONTROL_SKILLS,
                                                )

    def run(self):
        start_up()
        while True:
            self._process()

    def _process(self):
        self.skill_controller.wake_up_check()
        if self.skill_controller.is_assistant_enabled:  # Check if the assistant is waked up
            self.skill_controller.get_transcript()
            self.skill_controller.get_skills()
            if self.skill_controller.to_execute:
                response = self.response_creator.create_positive_response(
                    self.skill_controller.to_execute['voice_transcript'])
            else:
                response = self.response_creator.create_negative_response(
                    self.skill_controller.to_execute['voice_transcript'])
            self.output_engine.assistant_response(response)
            self.skill_controller.execute()
