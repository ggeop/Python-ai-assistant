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

from jarvis.utils.application_utils import OutputStyler, console_output
from jarvis.settings import GENERAL_SETTINGS
from jarvis.utils import application_utils
from jarvis.setup import engine
from jarvis.core import controller


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

    # Add the rest of word in a batch
    if letter_id < len(raw_text):
        list_of_batches.append(raw_text[letter_id:])
    return list_of_batches


def speech(text):
    """
    Speech method translate text batches to speech
    :param text: string (e.g 'tell me about google')
    """

    cumulative_batch = ''
    for batch in _create_text_batches(raw_text=text):
        engine.say(batch)
        cumulative_batch += batch
        console_output(cumulative_batch)
        try:
            engine.runAndWait()
        except RuntimeError:
            pass
        if controller.ControllingState.stop_speaking:
            controller.ControllingState.stop_speaking = False
            break


def assistant_response(text):
    """
    Assistant response in voice or/and in text.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_speech']:
        application_utils.stop_speaking = False
        try:
            speech_tread = threading.Thread(target=speech, args=[text])
            speech_tread.start()
        except RuntimeError:
            pass
    else:
        console_output(text)


def user_speech_playback(text):
    """
    Prints the user commands in text.
    :param text: string
    """
    print(application_utils.user_input)


def stdout_print(text):
    """
    Application stdout with format.
    :param text: string
    """
    print(OutputStyler.CYAN + text + OutputStyler.ENDC)