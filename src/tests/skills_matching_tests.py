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
from unittest.mock import patch

from jarvis.core.processor import Processor
from jarvis import settings
from jarvis.utils.mongoDB import db
from jarvis.skills.skills_registry import BASIC_SKILLS
from jarvis.enumerations import MongoCollections


def get_skill_name_from_call_args(call_agrs):
    return call_agrs[0][0]['skill']['name']


@patch('jarvis.core.processor.Processor._execute_skill')
@patch('jarvis.core.processor.engines.TTTEngine')
class TestSkillMatching(unittest.TestCase):

    def setUp(self):
        default_assistant_name = settings.DEFAULT_GENERAL_SETTINGS['assistant_name']
        default_enabled_period = settings.DEFAULT_GENERAL_SETTINGS['enabled_period']
        default_input_mode = settings.DEFAULT_GENERAL_SETTINGS['input_mode']
        default_response_in_speech = settings.DEFAULT_GENERAL_SETTINGS['response_in_speech']

        default_settings = {
            'assistant_name': default_assistant_name,
            'enabled_period': default_enabled_period,
            'input_mode': default_input_mode,
            'response_in_speech': default_response_in_speech,
        }

        db.update_collection(collection=MongoCollections.GENERAL_SETTINGS.value, documents=[default_settings])

        # Add assistant name in  skill 'enable_assistant' + 'assistant_check' tags
        assistant_name = db.get_documents(collection=MongoCollections.GENERAL_SETTINGS.value)[0]['assistant_name']

        # Update enable_assistant skill
        existing_enable_assistant_tags = db.get_documents(collection=MongoCollections.CONTROL_SKILLS.value,
                                                          key={'name': 'enable_assistant'})[0]['tags']
        new_enable_assistant_tags = {'tags': existing_enable_assistant_tags + ' ' + assistant_name}
        db.update_document(collection=MongoCollections.CONTROL_SKILLS.value,
                           query={'name': 'enable_assistant'},
                           new_value=new_enable_assistant_tags
                           )

        # Update assistant_check
        existing_assistant_check_tags = db.get_documents(collection=MongoCollections.ENABLED_BASIC_SKILLS.value,
                                                         key={'name': 'assistant_check'})[0]['tags']
        new_assistant_check_tags = {'tags': existing_assistant_check_tags + ' ' + assistant_name}
        db.update_document(collection=MongoCollections.ENABLED_BASIC_SKILLS.value,
                           query={'name': 'assistant_check'},
                           new_value=new_assistant_check_tags
                           )


    def test_all_skill_matches(self, mocked_ttt_engine, mocked_execute_skill):
        """
        In this test we examine the matches or  ALL skill tags with the functions
        If all skills matched right then the test passes otherwise not.

        At the end we print a report with all the not matched cases.

        """

        verifications_errors = []

        self.processor = Processor(settings, db)
        mocked_ttt_engine.return_value.recognize_input.return_value = 'hi'
        self.processor.run()

        for basic_skill in BASIC_SKILLS:
            print('--------------------------------------------------------------------------------------')
            print('Examine skill: {0}'.format(basic_skill.get('name')))
            for tag in basic_skill.get('tags',).split(','):
                # If the skill has matching tags
                if tag:
                    mocked_ttt_engine.return_value.recognize_input.return_value = tag
                    self.processor.run()
                    expected_skill = basic_skill.get('name')
                    actual_skill = get_skill_name_from_call_args(mocked_execute_skill.call_args)
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
