import unittest
from unittest.mock import patch

from jarvis.command_controller import CommandController
from jarvis.settings import TRIGGERING_WORDS


class CommandControllerTests(unittest.TestCase):

    @patch('jarvis.action_controller.subprocess.Popen')
    def test_execute_commands(self, mocked_Popen):
        commands = {TRIGGERING_WORDS['open_browser']}
        words = 'open youtube'
        CommandController._execute_commands(commands, words)
        self.assertEqual(1, mocked_Popen.call_count)
