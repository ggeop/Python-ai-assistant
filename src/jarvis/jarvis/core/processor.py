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

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from jarvis.core.controller import SkillController
from jarvis.utils.general_utils import start_up
from jarvis.settings import GENERAL_SETTINGS, ANALYZER_CONF
from jarvis.skills.skills_registry import CONTROL_SKILLS, SKILLS
from jarvis.skills.skill_analyzer import SkillAnalyzer
from jarvis.settings import SPEECH_RECOGNITION
from jarvis.engines.stt import STTEngine
from jarvis.engines.ttt import TTTEngine


class Processor:
    def __init__(self):
        self.skill_analyzer = SkillAnalyzer(
                                            weight_measure=TfidfVectorizer,
                                            similarity_measure=cosine_similarity,
                                            args=ANALYZER_CONF,
                                            skills_=SKILLS,
                                            )

        self.input_engine = STTEngine(
                                        pause_threshold=SPEECH_RECOGNITION['pause_threshold'],
                                        energy_theshold=SPEECH_RECOGNITION['energy_threshold'],
                                        ambient_duration=SPEECH_RECOGNITION['ambient_duration'],
                                        dynamic_energy_threshold=SPEECH_RECOGNITION['dynamic_energy_threshold'],
                                        sr=sr
                                        ) if GENERAL_SETTINGS['user_voice_input'] else TTTEngine()

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
            self.skill_controller.execute()
