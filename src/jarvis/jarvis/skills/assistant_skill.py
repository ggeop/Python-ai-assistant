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
import speech_recognition as sr

from jarvis.core.console_manager import ConsoleManager
from jarvis.utils.mongoDB import db
from jarvis.settings import SPEECH_RECOGNITION
from jarvis.enumerations import InputMode
import jarvis.engines as engines


class AssistantSkill:
    """
    This class is the parent of all skill classes.
    """
    first_activation = True
    console_manager = ConsoleManager()
    engine = None
    input_engine = engines.STTEngine(
        pause_threshold=SPEECH_RECOGNITION.get('pause_threshold'),
        energy_theshold=SPEECH_RECOGNITION.get('energy_threshold'),
        ambient_duration=SPEECH_RECOGNITION.get('ambient_duration'),
        dynamic_energy_threshold=SPEECH_RECOGNITION.get(
            'dynamic_energy_threshold'),
        sr=sr
    ) if db.get_documents(collection='general_settings')[0]['input_mode'] == InputMode.VOICE.value \
        else engines.TTTEngine()

    @classmethod
    def console(cls, text):
        cls.console_manager.console_output(text)

    @classmethod
    def response(cls, text):
        cls.set_engine()
        cls.engine.assistant_response(text)

    @classmethod
    def extract_tags(cls, voice_transcript, tags):
        """
        This method identifies the tags from the user transcript for a specific skill.

        e.x
        Let's that the user says "hi jarvis!".
        The skill analyzer will match it with enable_assistant skill which has tags 'hi, hello ..'
        This method will identify the that the enabled word was the 'hi' not the hello.

        :param voice_transcript: string
        :param tags: string
        :return: set
        """
        try:
            transcript_words = voice_transcript.split()
            tags = tags.split(',')
            return set(transcript_words).intersection(tags)
        except Exception as e:
            logging.error("Failed to extract tags with message {0}".format(e))
            return set()

    @classmethod
    def set_engine(cls):
        if not cls.engine and not db.is_collection_empty(collection='general_settings'):
            cls.engine = engines.TTSEngine() if db.get_documents(collection='general_settings')[0]['response_in_speech']\
                    else engines.TTTEngine()
