import unittest
from unittest.mock import patch, MagicMock

from jarvis.command_manager import CommandManager
from jarvis.settings import TRIGGERING_WORDS


class CommandControllerTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.command_controller = CommandManager()

    @patch('jarvis.command_manager.CommandManager._record')
    @patch('jarvis.command_manager.sr.Microphone')
    @patch('jarvis.command_manager.sr.Recognizer.recognize_google')
    @patch('jarvis.command_manager.CommandManager._get_voice_transcript')
    def test_wake_up(self, mocked_get_words, mocked_recognize_google, mocked_microphone, mocked_record):
        mocked_recognize_google.return_value = 'can you '
        self.assertEqual(False, self.command_controller.wake_up_check())

        mocked_recognize_google.return_value = 'can you ' + TRIGGERING_WORDS['enable_jarvis']
        self.assertEqual(True, self.command_controller.wake_up_check())

    @patch('jarvis.action_manager.ActionManager.open_website_in_browser')
    @patch('jarvis.command_manager.CommandManager._record')
    @patch('jarvis.command_manager.sr.Microphone')
    @patch('jarvis.action_manager.subprocess.Popen')
    def test_execute_commands(self, mocked_Popen, mocked_microphone, mocked_record, mocked_open_website):

        commands = {}
        self.command_controller._execute_commands(commands)
        self.assertEqual(0, mocked_Popen.call_count)

        commands = {TRIGGERING_WORDS['open_browser']}
        self.command_controller.words = 'open youtube'
        self.command_controller._execute_commands(commands)
        self.assertEqual(1, mocked_Popen.call_count)



