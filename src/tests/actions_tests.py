import unittest
from unittest.mock import patch

from jarvis.actions import Actions


class ActionsTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.actions = Actions()

    @patch('jarvis.actions.Actions._ready_to_start')
    @patch('jarvis.actions.Actions._continue_listening')
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
    @patch('jarvis.action_manager.Skills.disable_jarvis')
    def test_execute_commands(self, mocked_exit, mocked_disable_jarvis):

        self.actions.latest_voice_transcript = ' '
        self.actions.shutdown_check()
        self.assertEqual(0, mocked_disable_jarvis.call_count)

        self.actions.latest_voice_transcript = 'stop stop'
        self.actions.shutdown_check()
        self.assertEqual(1, mocked_disable_jarvis.call_count)

    @patch('jarvis.actions.Actions.get_transcript')
    @patch('jarvis.action_manager.Skills.enable_jarvis')
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
