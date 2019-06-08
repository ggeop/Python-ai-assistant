import unittest
from unittest.mock import patch
from jarvis.skills.skills import Skills


class SkillsTests(unittest.TestCase):

    @patch('jarvis.action_manager.wikipedia.page')
    def test_tell_me_about(self, mocked_wiki):
        words = 'tell me about google'
        Skills.tell_me_about(voice_transcript=words, skill=None, tag='about')
        self.assertEqual(1, mocked_wiki.call_count)
        words = 'about google'
        self.assertRaises(Exception, Skills.tell_me_about(voice_transcript=words, skill=None, tag='about'))
