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

import unittest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from jarvis import settings
from jarvis.skills.registry import CONTROL_SKILLS, BASIC_SKILLS, ENABLED_BASIC_SKILLS
from jarvis.enumerations import MongoCollections
from jarvis.skills.analyzer import SkillAnalyzer
from jarvis.utils.mongoDB import db


class TestSkillMatching(unittest.TestCase):

    def setUp(self):

        all_skills = {
            MongoCollections.CONTROL_SKILLS.value: CONTROL_SKILLS,
            MongoCollections.ENABLED_BASIC_SKILLS.value: ENABLED_BASIC_SKILLS,
        }
        for collection, documents in all_skills.items():
            db.update_collection(collection, documents)

        default_assistant_name = settings.DEFAULT_GENERAL_SETTINGS['assistant_name']
        default_input_mode = settings.DEFAULT_GENERAL_SETTINGS['input_mode']
        default_response_in_speech = settings.DEFAULT_GENERAL_SETTINGS['response_in_speech']

        default_settings = {
            'assistant_name': default_assistant_name,
            'input_mode': default_input_mode,
            'response_in_speech': default_response_in_speech,
        }

        db.update_collection(collection=MongoCollections.GENERAL_SETTINGS.value, documents=[default_settings])

        self.skill_analyzer = SkillAnalyzer(
                                            weight_measure=TfidfVectorizer,
                                            similarity_measure=cosine_similarity,
                                            args=settings.SKILL_ANALYZER.get('args'),
                                            sensitivity=settings.SKILL_ANALYZER.get('sensitivity'),
                                            )

    def test_all_skill_matches(self):
        """
        In this test we examine the matches or  ALL skill tags with the functions
        If all skills matched right then the test passes otherwise not.

        At the end we print a report with all the not matched cases.

        """

        verifications_errors = []

        for basic_skill in BASIC_SKILLS:
            print('--------------------------------------------------------------------------------------')
            print('Examine skill: {0}'.format(basic_skill.get('name')))
            for tag in basic_skill.get('tags',).split(','):
                # If the skill has matching tags
                if tag:
                    expected_skill = basic_skill.get('name')
                    actual_skill = self.skill_analyzer.extract(tag).get('name')
                    try:
                        self.assertEqual(expected_skill, actual_skill)
                    except AssertionError as e:
                        verifications_errors.append({'tag': tag, 'error': e})

        print('-------------------------------------- SKILLS MATCHING REPORT --------------------------------------')
        if verifications_errors:
            for increment, e in enumerate(verifications_errors):
                print('{0})'.format(increment))
                print('Not correct match with tag: {0}'.format(e.get('tag')))
                print('Assertion values (expected != actual): {0}'.format(e.get('error')))
            raise AssertionError
        else:
            print('All skills matched correctly!')
