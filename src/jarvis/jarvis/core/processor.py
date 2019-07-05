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

from jarvis.core.controller import SkillsController
from jarvis.utils.application_utils import start_up
from jarvis.settings import GENERAL_SETTINGS
from jarvis.skills.skills_registry import CONTROL_SKILLS, SKILLS
from jarvis.core.analyzer import Analyzer
from jarvis.settings import SPEECH_RECOGNITION
from jarvis.engines.stt import STTEngine


args = {
    "stop_words": "english",
    "lowercase": True,
    "norm": 'l1',
    "use_idf": True,
}


class Processor:
    def __init__(self):
        self.analyzer = Analyzer(weight_measure=TfidfVectorizer,
                                 similarity_measure=cosine_similarity,
                                 args=args,
                                 skills_=SKILLS
                                 )
        self.stt_engine = STTEngine(pause_threshold=SPEECH_RECOGNITION['pause_threshold'],
                                    energy_theshold=SPEECH_RECOGNITION['energy_threshold'],
                                    ambient_duration=SPEECH_RECOGNITION['ambient_duration'],
                                    dynamic_energy_threshold=SPEECH_RECOGNITION['dynamic_energy_threshold'],
                                    speech_recognizer=sr)

        self.controller = SkillsController(settings_=GENERAL_SETTINGS,
                                           stt_engine=self.stt_engine,
                                           analyzer=self.analyzer,
                                           control_skills=CONTROL_SKILLS
                                           )

    def run(self):
        start_up()
        while True:
            self._process()

    def _process(self):
        # Check if the assistant is waked up
        if self.controller.wake_up_check():

            self.controller.get_transcript()
            self.controller.get_skills()

            if self.controller.to_execute:
                self.controller.execute()
