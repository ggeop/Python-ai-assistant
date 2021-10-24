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

import logging
from jarvis.core.console import ConsoleManager
from jarvis.utils.console import user_input


class TTTEngine:
    """
    Text To Text Engine (TTT)
    """
    def __init__(self):
        self.logger = logging
        self.console_manager = ConsoleManager()

    def recognize_input(self, **kwargs):
        """
        Recognize input from console and returns transcript if its not empty string.
        """
        try:
            text_transcript = input(user_input).lower()
            while text_transcript == '':
                text_transcript = input(user_input).lower()
            return text_transcript
        except EOFError as e:
            self.console_manager.console_output(error_log='Failed to recognize user input with message: {0}'.format(e))

    def assistant_response(self, message, refresh_console=True):
        """
        Assistant response in voice or/and in text.
        :param refresh_console: boolean
        :param message: string
        """
        try:
            if message:
                self.console_manager.console_output(message, refresh_console=refresh_console)
        except RuntimeError as e:
            self.console_manager.console_output(error_log='Error in assistant response with message: {0}'.format(e))
