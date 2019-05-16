import unittest
from unittest.mock import patch

from assistant.command_controller import CommandController
from assistant.settings import BROWSER_TRIGGERING_WORD


class CommandControllerTests(unittest.TestCase):

    @patch('assistant.action_controller.subprocess.Popen')
    def test_execute_commands(self, mocked_Popen):
        commands = {BROWSER_TRIGGERING_WORD}
        words = 'open youtube'
        CommandController.execute_commands(commands, words)
        self.assertEqual(1, mocked_Popen.call_count)


