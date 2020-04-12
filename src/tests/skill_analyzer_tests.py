# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
from unittest.mock import patch

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from jarvis.skills.skill_analyzer import SkillAnalyzer
from jarvis.utils.mongoDB import MongoDB, start_mongoDB_server, stop_mongoDB_server
from jarvis.settings import *
from jarvis.skills.datetime import DatetimeSkills
from jarvis.skills.internet import InternetSkills


class SkillTests(unittest.TestCase):

    def setUp(self):
        start_mongoDB_server()
        db = MongoDB()
        self.skill_analyzer = SkillAnalyzer(
            weight_measure=TfidfVectorizer,
            similarity_measure=cosine_similarity,
            args=SKILL_ANALYZER.get('args'),
            sensitivity=SKILL_ANALYZER.get('sensitivity'),
            db=db
        )

    def tearDown(self):
        stop_mongoDB_server()

    def test_extract(self):
        """
        Test few extraction cases on basic skills
        """

        # Internet skill extraction
        tell_date_func_name = InternetSkills.internet_availability.__name__
        internet_conenction_tag = 'internet conection'
        extracted_internet_conenction_func_name = self.skill_analyzer.extract(internet_conenction_tag).get('func')
        self.assertEqual(tell_date_func_name, extracted_internet_conenction_func_name)

        # Time skill extraction
        tell_time_func_name = DatetimeSkills.tell_the_time.__name__
        time_tag = 'time'
        extracted_time_func_name = self.skill_analyzer.extract(time_tag).get('func')
        self.assertEqual(tell_time_func_name, extracted_time_func_name)

        # Date skill extraction
        tell_date_func_name = DatetimeSkills.tell_the_date.__name__
        date_tag = 'date'
        extracted_date_func_name = self.skill_analyzer.extract(date_tag).get('func')
        self.assertEqual(tell_date_func_name, extracted_date_func_name)
