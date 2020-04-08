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
from jarvis.core.console_manager import ConsoleManager


class TTTEngine:
    """
    Text To Text Engine (TTT)
    """
    def __init__(self):
        self.logger = logging
        self.console_manager = ConsoleManager()

    def recognize_input(self):
        self.logger.info("Waiting for user input.")
        text_transcript = input('>> ').lower()
        while text_transcript == '':
            self.logger.info("User didn't said something")
            text_transcript = input('>> ').lower()
        return text_transcript

    def assistant_response(self, message):
        """
        Assistant response in voice or/and in text.
        :param message: string
        """
        try:
            if message:
                self.console_manager.console_output(message)
        except RuntimeError as e:
            self.logger.error('Error in assistant response with message {0}'.format(e))
