import unittest
from unittest.mock import patch

from jarvis.action_controller import ActionController


class CommandControllerTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.action_controller = ActionController()

    @patch('jarvis.action_controller.ActionController._ready_to_start')
    @patch('jarvis.action_controller.ActionController._continue_listening')
    def test_wake_up(self, mocked_ready_to_start, mocked_continue_listening):

        self.action_controller.execute_state = {'ready_to_execute': False, 'enable_time': None}
        mocked_ready_to_start.return_value = False
        mocked_continue_listening.return_value = False
        self.assertEqual(False, self.action_controller.wake_up_check())

        self.action_controller.execute_state = {'ready_to_execute': False, 'enable_time': None}
        mocked_ready_to_start.return_value = False
        mocked_continue_listening.return_value = True
        self.assertEqual(True, self.action_controller.wake_up_check())

        self.action_controller.execute_state = {'ready_to_execute': True, 'enable_time': None}
        mocked_ready_to_start.return_value = True
        self.assertEqual(True, self.action_controller.wake_up_check())

        self.action_controller.execute_state = {'ready_to_execute': True, 'enable_time': None}
        mocked_ready_to_start.return_value = False
        self.assertEqual(False, self.action_controller.wake_up_check())

    @patch('jarvis.action_manager.sys.exit')
    @patch('jarvis.action_manager.ActionManager.disable_jarvis')
    def test_execute_commands(self, mocked_exit, mocked_disable_jarvis):

        self.action_controller.latest_voice_transcript = ' '
        self.action_controller.shutdown_check()
        self.assertEqual(0, mocked_disable_jarvis.call_count)

        self.action_controller.latest_voice_transcript = 'stop stop'
        self.action_controller.shutdown_check()
        self.assertEqual(1, mocked_disable_jarvis.call_count)

    @patch('jarvis.action_controller.ActionController.get_voice_transcript')
    @patch('jarvis.action_manager.ActionManager.enable_jarvis')
    def test_ready_to_start(self, mocked_get_voiced_transcript, mocked_enable_jarvis):
        self.action_controller.latest_voice_transcript = '..'
        self.assertEqual(None, self.action_controller._ready_to_start())

        self.action_controller.latest_voice_transcript = 'hi'
        mocked_enable_jarvis.return_value = {'ready_to_execute': True, 'enable_time': 'now'}
        self.assertEqual(True, self.action_controller._ready_to_start())

    def test_continue_listening(self):
        pass

    def test_get_user_actions(self):
        self.action_controller.latest_voice_transcript = 'open open time'
        self.action_controller.get_user_actions()
        self.assertEqual(2, len(self.action_controller.actions_to_execute))
