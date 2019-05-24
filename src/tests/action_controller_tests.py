import unittest
from unittest.mock import patch, MagicMock

from jarvis.action_controller import ActionController
from jarvis.actions_registry import ACTIONS, CONTROL_ACTIONS


class CommandControllerTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.action_controller = ActionController()

    @patch('jarvis.action_controller.ActionController._record')
    @patch('jarvis.action_controller.sr.Microphone')
    @patch('jarvis.action_controller.sr.Recognizer.recognize_google')
    @patch('jarvis.action_controller.ActionController._get_voice_transcript')
    def test_wake_up(self, mocked_get_words, mocked_recognize_google, mocked_microphone, mocked_record):
        mocked_recognize_google.return_value = 'can you '
        self.assertEqual(None, self.action_controller.wake_up_check())

        mocked_recognize_google.return_value = 'can you ' + list(CONTROL_ACTIONS['enable_jarvis']['tags'])[0]
        self.assertEqual(True, self.action_controller.wake_up_check())

    @patch('jarvis.action_manager.ActionManager.open_website_in_browser')
    @patch('jarvis.command_manager.CommandManager._record')
    @patch('jarvis.command_manager.sr.Microphone')
    @patch('jarvis.action_manager.subprocess.Popen')
    def test_execute_commands(self, mocked_Popen, mocked_microphone, mocked_record, mocked_open_website):

        commands = {}
        self.action_controller._execute_commands(commands)
        self.assertEqual(0, mocked_Popen.call_count)

        commands = {TRIGGERING_WORDS['open_browser']}
        self.action_controller.words = 'open youtube'
        self.action_controller._execute_commands(commands)
        self.assertEqual(1, mocked_Popen.call_count)



