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

from jarvis.utils.console_utils import user_input, clear


class STTEngine:
    """
    Speech To Text Engine (STT)
    """
    def __init__(self, pause_threshold, energy_theshold, ambient_duration, dynamic_energy_threshold, sr):
        self.logger = logging
        self.sr = sr
        self.speech_recognizer = sr.Recognizer()
        self.dynamic_energy_ratio = self.speech_recognizer.dynamic_energy_ratio
        self.dynamic_energy_threshold = self.speech_recognizer.energy_threshold
        self.microphone = self._set_microphone(
                                              pause_threshold=pause_threshold,
                                              energy_threshold=energy_theshold,
                                              ambient_duration=ambient_duration,
                                              dynamic_energy_threshold=dynamic_energy_threshold
                                              )

    def recognize_input(self):
        """
        Capture the words from the recorded audio (audio stream --> free text).
        """
        audio_text = self._record()
        try:
            voice_transcript = self.speech_recognizer.recognize_google(audio_text)
            self.logger.debug('Recognized words: ' + voice_transcript)
            return voice_transcript
        except self.sr.UnknownValueError:
            self.logger.info('Not recognized text')
        except self.sr.RequestError:
            self.logger.info("Google API was unreachable.")

    def _record(self):
        """
        Capture the user speech and transform it to audio stream (speech --> audio stream --> text).
        """
        self._update_microphone_noise_level()

        with self.microphone as source:
            audio_text = self.speech_recognizer.listen(source)
        return audio_text

    def _update_microphone_noise_level(self):
        """
        Update microphone variables in assistant state.
        """
        self.dynamic_energy_ratio = self.speech_recognizer.dynamic_energy_ratio  # Update dynamic energy ratio
        self.energy_threshold = self.speech_recognizer.dynamic_energy_threshold  # Update microphone energy threshold

        self.logger.debug("Dynamic energy ration value is: {0}".format(self.dynamic_energy_ratio))
        self.logger.debug("Energy threshold is: {0}".format(self.energy_threshold))

    def _set_microphone(self, pause_threshold, energy_threshold, ambient_duration, dynamic_energy_threshold):
        """
        Setup the assistant microphone.
        """
        microphone_list = self.sr.Microphone.list_microphone_names()

        clear()
        print("=" * 48)
        print("Microphone Setup")
        print("=" * 48)
        print("Which microphone do you want to use a assistant mic:")

        for index, name in enumerate(microphone_list):
            print("{0}) Microphone: {1}".format(index, name))

        choices = "Choice[1-{0}]: ".format(len(microphone_list))
        print("WARNING: "
              "In case of error of 'Invalid number of channels' try again with different micrphone choice")
        index = input(choices)

        while not index.isnumeric():
            index = input("Please select a number between choices[1-{0}]: ".format(len(microphone_list)))

        with self.sr.Microphone(device_index=int(index), chunk_size=512) as source:
            self.speech_recognizer.pause_threshold = pause_threshold
            self.speech_recognizer.energy_threshold = energy_threshold

            clear()
            print("-" * 48)
            print("Microphone Calibration")
            print("-" * 48)

            print("Please wait.. for {} seconds ".format(ambient_duration))
            self.speech_recognizer.adjust_for_ambient_noise(source, duration=ambient_duration)
            self.speech_recognizer.dynamic_energy_threshold = dynamic_energy_threshold
            print("Microphone calibrated successfully!")

            return source
