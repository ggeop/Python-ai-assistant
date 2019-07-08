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

import threading
import logging
import pyttsx3
import time

class TTSEngine:
    """
    Text To Speech Engine (TTS)
    """
    def __init__(self, console_manager, speech_response_enabled):
        self.logger = logging
        self.console_manager = console_manager
        self.speech_response_enabled = speech_response_enabled
        self.stop_speaking = False
        self.engine_ = self._set_voice_engine()

    def assistant_response(self, text):
        """
        Assistant response in voice or/and in text.
        :param text: string
        """
        if self.speech_response_enabled:
            try:
                speech_tread = threading.Thread(target=self._speech_and_console, args=[text])
                speech_tread.start()
            except RuntimeError as e:
                self.logger.error('Error in assistant response thread with message {0}'.format(e))

    def _speech_and_console(self, text):
        """
        Speech method translate text batches to speech and print them in the console.
        :param text: string (e.g 'tell me about google')
        """
        cumulative_batch = ''
        if text:
            for batch in self._create_text_batches(raw_text=text):
                self.engine_.say(batch)
                cumulative_batch += batch
                self.console_manager.console_output(cumulative_batch)
                try:
                    self.engine_.runAndWait()
                except RuntimeError:
                    pass
                if self.stop_speaking:
                    self.logger.debug('Speech interruption triggered')
                    self.stop_speaking = False
                    break

    @staticmethod
    def _create_text_batches(raw_text, number_of_words_per_batch=5):
        """
        Splits the user speech into batches and return a list with the split batches
        :param raw_text: string
        :param number_of_words_per_batch: int
        :return: list
        """
        raw_text = raw_text + ' '
        list_of_batches = []
        total_words = raw_text.count(' ')
        letter_id = 0

        for split in range(0, int(total_words / number_of_words_per_batch)):
            batch = ''
            words_count = 0
            while words_count < number_of_words_per_batch:
                batch += raw_text[letter_id]
                if raw_text[letter_id] == ' ':
                    words_count += 1
                letter_id += 1
            list_of_batches.append(batch)

        if letter_id < len(raw_text):  # Add the rest of word in a batch
            list_of_batches.append(raw_text[letter_id:])
        return list_of_batches

    @staticmethod
    def _set_voice_engine():
        """
        Setup text to speech engine
        :return: gtts engine object
        """
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 160)  # Setting up new voice rate
        tts_engine.setProperty('volume', 1.0)  # Setting up volume level  between 0 and 1
        return tts_engine
