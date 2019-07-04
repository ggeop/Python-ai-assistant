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

from jarvis.core.memory import State
from jarvis.utils.application_utils import user_input, speech_interruption


class STTEngine:
    def __init__(self, speech_recognizer=None, microphone=None):
        self.logger = logging
        self.speech_recognizer = speech_recognizer
        self.microphone = microphone

    def recognize_text(self):
        self.logger.info("Waiting for user input..")
        voice_transcript = input(user_input).lower()
        while voice_transcript == '':
            print("Say something..")
            voice_transcript = input(user_input).lower()
        # if speech_interruption(self.latest_voice_transcript):
        #     self.latest_voice_transcript = ''
        #     self.logger.debug('Speech interruption')
        return voice_transcript

    def recognize_voice(self):
        """
        Records voice and update latest_voice_transcript with the latest user speech.
        """
        audio_text = self._record()
        try:
            # self.voice_transcript = self.speech_recognizer.recognize_google(audio_text).lower()
            voice_transcript = audio_text.lower()
            self.logger.debug('Recognized words: ' + voice_transcript)
            # if speech_interruption(self.latest_voice_transcript):
            #     voice_transcript = ''
            #     self.logger.debug('User Speech interruption')
            return voice_transcript
        except sr.UnknownValueError:
            print('....')
        except sr.RequestError:
            print("Try later.. (Google API was unreachable..)")

    def _record(self):
        """
        Capture the user speech and transform it to audio stream (speech --> audio stream --> text).
        """

        self._update_microphone_noise_level()

        with self.microphone as source:
            audio_text = self.speech_recognizer.listen(source)
            audio_text = input("input: ")
        return audio_text

    def _update_microphone_noise_level(self):
        """
        Update microphone variables in assistant state.
        """
        #  Update dynamic energy ratio
        State.dynamic_energy_ratio = self.speech_recognizer.dynamic_energy_ratio
        self.logger.debug('Dynamic energy ration value is: {0}'.format(State.dynamic_energy_ratio))

        #  Update microphone energy threshold
        State.energy_threshold = self.speech_recognizer.energy_threshold
        self.logger.debug('Energy threshold is: {0}'.format(State.energy_threshold))