import unittest
from unittest.mock import patch

from jarvis.action_controller import ActionController


class ActionControllerTests(unittest.TestCase):

    @patch('jarvis.command_controller.get_words')
    def test_wake_up(self, mocked_get_words):
        self.assertEqual(True, ActionController.wake_up('There is a hello in the sentence'))
        self.assertEqual(None, ActionController.wake_up('Sentence with no the triggering word'))

    @patch('jarvis.action_controller.wikipedia.page')
    def test_tell_me_about(self, mocked_wiki):
        words = 'tell me about google'
        ActionController.tell_me_about(words)
        self.assertEqual(1, mocked_wiki.call_count)
        words = 'about google'
        self.assertRaises(Exception, ActionController.tell_me_about(words))
