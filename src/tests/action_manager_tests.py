import os
import sys

src_path = os.path.join(sys.path[0], '..')
config_path = os.path.join(src_path, 'jarvis', 'config.conf')
sys.path.insert(3, config_path)

import unittest
from unittest.mock import patch
from jarvis.action_manager import ActionManager


class ActionControllerTests(unittest.TestCase):

    @patch('jarvis.action_manager.wikipedia.page')
    def test_tell_me_about(self, mocked_wiki):
        words = 'tell me about google'
        ActionManager.tell_me_about(words)
        self.assertEqual(1, mocked_wiki.call_count)
        words = 'about google'
        self.assertRaises(Exception, ActionManager.tell_me_about(words))
