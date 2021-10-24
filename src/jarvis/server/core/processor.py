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

import jarvis

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from jarvis.skills.analyzer import SkillAnalyzer
from jarvis.skills.registry import skill_objects
from jarvis.core.nlp import ResponseCreator
from jarvis.skills.collection.activation import ActivationSkills
from jarvis.utils.mongoDB import db
from jarvis.skills.collection.wolframalpha import WolframSkills


class Processor:
    def __init__(self, console_manager, settings_):
        self.console_manager = console_manager
        self.settings = settings_
        self.response_creator = ResponseCreator()
        self.skill_analyzer = SkillAnalyzer(
            weight_measure=TfidfVectorizer,
            similarity_measure=cosine_similarity,
            args=self.settings.SKILL_ANALYZER.get('args'),
            sensitivity=self.settings.SKILL_ANALYZER.get('sensitivity'),
        )

    def run(self):
        """
         Assistant starting point.

        - STEP 1: Get user input based on the input mode (voice or text)
        - STEP 2: Matches the input with a skill
        - STEP 3: Create a response
        - STEP 4: Execute matched skill
        - STEP 5: Insert user transcript and response in history collection (in MongoDB)

        """

        transcript = jarvis.input_engine.recognize_input()
        skill = self.skill_analyzer.extract(transcript)

        if skill:
            # ----------------------------------------------------------------------------------------------------------
            # Successfully extracted skill
            # ----------------------------------------------------------------------------------------------------------

            # ---------------
            # Positive answer
            # ---------------
            response = self.response_creator.create_positive_response(transcript)
            jarvis.output_engine.assistant_response(response)

            # ---------------
            # Skill execution
            # ---------------
            skill_to_execute = {'voice_transcript': transcript, 'skill': skill}
            self._execute_skill(skill_to_execute)

        else:
            # ----------------------------------------------------------------------------------------------------------
            # No skill extracted
            # ----------------------------------------------------------------------------------------------------------

            # ---------------
            # Negative answer
            # ---------------
            response = self.response_creator.create_negative_response(transcript)
            jarvis.output_engine.assistant_response(response)

            # ---------------
            # WolframAlpha API Call
            # ---------------
            skill_to_execute = {'voice_transcript': transcript,
                                'skill': {'name': WolframSkills.call_wolframalpha.__name__}
                                }

            response = WolframSkills.call_wolframalpha(transcript)

        # --------------------------------------------------------------------------------------------------------------
        # Add new record to history
        # --------------------------------------------------------------------------------------------------------------

        record = {'user_transcript': transcript,
                  'response': response if response else '--',
                  'executed_skill': skill_to_execute if skill_to_execute else '--'
                  }

        db.insert_many_documents('history', [record])

    def _execute_skill(self, skill):
        if skill:
            skill_func_name = skill.get('skill').get('func')
            self.console_manager.console_output(info_log='Executing skill {0}'.format(skill_func_name))
            try:
                ActivationSkills.enable_assistant()
                skill_func_name = skill.get('skill').get('func')
                skill_func = skill_objects[skill_func_name]
                skill_func(**skill)
            except Exception as e:
                self.console_manager.console_output(error_log="Failed to execute skill {0} with message: {1}"
                                                    .format(skill_func_name, e))
