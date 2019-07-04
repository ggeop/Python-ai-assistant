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

from jarvis.actions import Actions


class ActionsTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.actions = Actions()

    @patch('jarvis.actions.SkillsController._ready_to_start')
    @patch('jarvis.actions.SkillsController._continue_listening')
    def test_wake_up(self, mocked_ready_to_start, mocked_continue_listening):

        self.actions.execute_state = {'ready_to_execute': False, 'enable_time': None}
        mocked_ready_to_start.return_value = False
        mocked_continue_listening.return_value = False
        self.assertEqual(False, self.actions.wake_up_check())

        self.actions.execute_state = {'ready_to_execute': False, 'enable_time': None}
        mocked_ready_to_start.return_value = False
        mocked_continue_listening.return_value = True
        self.assertEqual(True, self.actions.wake_up_check())

        self.actions.execute_state = {'ready_to_execute': True, 'enable_time': None}
        mocked_ready_to_start.return_value = True
        self.assertEqual(True, self.actions.wake_up_check())

        self.actions.execute_state = {'ready_to_execute': True, 'enable_time': None}
        mocked_ready_to_start.return_value = False
        self.assertEqual(False, self.actions.wake_up_check())

    @patch('jarvis.action_manager.sys.exit')
    @patch('jarvis.action_manager.Skills.disable_assistant')
    def test_execute_commands(self, mocked_exit, mocked_disable_jarvis):

        self.actions.latest_voice_transcript = ' '
        self.actions.shutdown_check()
        self.assertEqual(0, mocked_disable_jarvis.call_count)

        self.actions.latest_voice_transcript = 'stop stop'
        self.actions.shutdown_check()
        self.assertEqual(1, mocked_disable_jarvis.call_count)

    @patch('jarvis.actions.SkillsController.get_transcript')
    @patch('jarvis.action_manager.Skills.enable_assistant')
    def test_ready_to_start(self, mocked_get_voiced_transcript, mocked_enable_jarvis):
        self.actions.latest_voice_transcript = '..'
        self.assertEqual(None, self.actions._ready_to_start())

        self.actions.latest_voice_transcript = 'hi'
        mocked_enable_jarvis.return_value = {'ready_to_execute': True, 'enable_time': 'now'}
        self.assertEqual(True, self.actions._ready_to_start())

    def test_continue_listening(self):
        pass

    def test_get_user_actions(self):
        self.actions.latest_voice_transcript = 'open open time'
        self.actions.get_skills()
        self.assertEqual(2, len(self.actions.skills_to_execute))
