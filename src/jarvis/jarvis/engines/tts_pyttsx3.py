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
import queue

from jarvis.core.console import ConsoleManager


class TTS:
    """
    Text To Speech Engine (TTS)
    """

    def __init__(self):
        self.tts_engine = self._set_voice_engine()

    def run_engine(self):
        try:
            self.tts_engine.runAndWait()
        except RuntimeError:
            pass

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


class TTSEngine(TTS):
    def __init__(self):
        super().__init__()
        self.logger = logging
        self.message_queue = queue.Queue(maxsize=9)  # Maxsize is the size of the queue / capacity of messages
        self.stop_speaking = False
        self.console_manager = ConsoleManager()

    def assistant_response(self, message, refresh_console=True):
        """
        Assistant response in voice.
        :param refresh_console: boolean
        :param message: string
        """
        self._insert_into_message_queue(message)
        try:
            speech_tread = threading.Thread(target=self._speech_and_console, args=(refresh_console,))
            speech_tread.start()
        except RuntimeError as e:
            self.logger.error('Error in assistant response thread with message {0}'.format(e))

    def _insert_into_message_queue(self, message):
        try:
            self.message_queue.put(message)
        except Exception as e:
            self.logger.error("Unable to insert message to queue with error message: {0}".format(e))

    def _speech_and_console(self, refresh_console):
        """
        Speech method translate text batches to speech and print them in the console.
        :param text: string (e.g 'tell me about google')
        """
        try:
            while not self.message_queue.empty():

                cumulative_batch = ''
                message = self.message_queue.get()
                if message:
                    batches = self._create_text_batches(raw_text=message)
                    for batch in batches:
                        self.tts_engine.say(batch)
                        cumulative_batch += batch
                        self.console_manager.console_output(cumulative_batch, refresh_console=refresh_console)
                        self.run_engine()
                        if self.stop_speaking:
                            self.logger.debug('Speech interruption triggered')
                            self.stop_speaking = False
                            break
        except Exception as e:
            self.logger.error("Speech and console error message: {0}".format(e))

    @staticmethod
    def _create_text_batches(raw_text, number_of_words_per_batch=8):
        """
        Splits the user speech message into batches and return a list with the split batches
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
