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

from jarvis.core.processor import Processor
from .test_settings import test_settings


def print_argument(argument):
    print(argument)


class E2ETests(unittest.TestCase):

    @patch('jarvis.core.processor.Processor._execute_skill', side_effect=print_argument)
    @patch('jarvis.core.processor.engines.TTTEngine')
    def test_run(self, mocked_ttt_engine, mocked_execute_skill):
        input_transcripts = ['hi', 'time', 'date', 'about']
        self.processor = Processor(test_settings)
        for transcipt in input_transcripts:
            mocked_ttt_engine.return_value.recognize_input.return_value = transcipt
            self.processor.run()


