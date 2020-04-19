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

from jarvis.skills.assistant_activation import ActivationSkills
from jarvis.skills.assistant_info import AssistantInfoSkills
from jarvis.utils.mongoDB import start_mongoDB_server, stop_mongoDB_server
from jarvis.enumerations import InputMode
from jarvis.skills.learn import Learn


class SkillTests(unittest.TestCase):

    def setUp(self):
        start_mongoDB_server()

    def tearDown(self):
        stop_mongoDB_server()

    # ------------------------------------------------------------------------------------------------------------------
    # Test assistant_activation skills
    # ------------------------------------------------------------------------------------------------------------------

    @patch('jarvis.skills.assistant_activation.play_activation_sound')
    @patch('jarvis.skills.assistant_activation.ActivationSkills.assistant_greeting')
    @patch('jarvis.skills.assistant_activation.db.get_documents')
    def test_enable_assistant(self, mocked_get_documents, mocked_assistant_greeting, mocked_play_activation_sound):
            mocked_get_documents.return_value = [{'input_mode': InputMode.VOICE.value}]
            ActivationSkills.enable_assistant()
            self.assertEqual(1, mocked_assistant_greeting.call_count)
            self.assertEqual(1, mocked_play_activation_sound.call_count)

            mocked_get_documents.return_value = [{'input_mode': InputMode.TEXT.value}]
            ActivationSkills.enable_assistant()
            self.assertEqual(2, mocked_assistant_greeting.call_count)
            self.assertEqual(1, mocked_play_activation_sound.call_count)

    @patch('jarvis.skills.assistant_activation.ActivationSkills.response')
    @patch('jarvis.skills.assistant_activation.clear')
    @patch('jarvis.skills.assistant_activation.stop_mongoDB_server')
    @patch('jarvis.skills.assistant_activation.sys.exit')
    def test_disable_assistant(self, mocked_exit, mocked_stop_mongoDB_server, mocked_clear, mocked_response):
        ActivationSkills.disable_assistant()
        self.assertEqual(1, mocked_exit.call_count)
        self.assertEqual(1, mocked_stop_mongoDB_server.call_count)
        self.assertEqual(1, mocked_clear.call_count)
        self.assertEqual(1, mocked_response.call_count)

    def test_assistant_greeting(self):
        ActivationSkills.assistant_greeting()

    # ------------------------------------------------------------------------------------------------------------------
    # Test assistant_info skills
    # ------------------------------------------------------------------------------------------------------------------

    @patch('jarvis.skills.assistant_info.AssistantInfoSkills.response')
    def test_assistant_check(self, mocked_response):
        AssistantInfoSkills.assistant_check()
        self.assertEqual(1, mocked_response.call_count)

    @patch('jarvis.skills.assistant_info.AssistantInfoSkills.response')
    def test_tell_the_skills(self, mocked_response):
        AssistantInfoSkills.tell_the_skills()

    def test_assistant_help(self):
        AssistantInfoSkills.assistant_help()

    # ------------------------------------------------------------------------------------------------------------------
    # Test learn skills
    # ------------------------------------------------------------------------------------------------------------------

    @patch('builtins.input', lambda *args: 'n')
    def test_learn_skill(self):
        Learn.learn()
