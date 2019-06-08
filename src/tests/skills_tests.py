import unittest
from unittest.mock import patch
from jarvis.skills.skill_manager import SkillManager


class SkillsTests(unittest.TestCase):

    @patch('jarvis.action_manager.wikipedia.page')
    def test_tell_me_about(self, mocked_wiki):
        words = 'tell me about google'
        SkillManager.tell_me_about(voice_transcript=words, skill=None, tag='about')
        self.assertEqual(1, mocked_wiki.call_count)
        words = 'about google'
        self.assertRaises(Exception, SkillManager.tell_me_about(voice_transcript=words, skill=None, tag='about'))
