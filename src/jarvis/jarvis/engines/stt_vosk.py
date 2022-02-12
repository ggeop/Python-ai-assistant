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

from cmath import inf
import logging

import jarvis
from jarvis.engines.stt import STTEngine
from jarvis.core.console import ConsoleManager
import sounddevice as sd
import vosk
import json
import sys
from types import SimpleNamespace
import queue
import os

# work_queue = queue.Queue()

# def other_callback(indata, frames, time, status):
#     print("Callback...")
#     if status:
#         print("Callback status: " + status)
#     work_queue.put(bytes(indata))

class STTEngineVosk(STTEngine):
    """
    Speech To Text Engine (STT)

    Vosk API Speech recognition settings
    SpeechRecognition API : https://pypi.org/project/SpeechRecognition/2.1.3
    """

    def __init__(self):
        super().__init__()
        self.console_manager.console_output(info_log="Initializing Vosk STT Engine")
        self.console_manager.console_output(info_log="Configuring Mic..")
        model_dir = 'model'
        device_id = 'default' #None
        device_info = sd.query_devices(device_id, 'input')
        self.sample_rate = int(device_info['default_samplerate'])
        if not os.path.exists(model_dir):
            self.console_manager.console_output(error_log="Model directory does not exist: {}".format(model_dir))
            exit(0)
        self.vosk_model = vosk.Model(model_dir) # default to a model directory of 'model'
        self.work_queue = queue.Queue()
        self.recognizer = vosk.KaldiRecognizer(self.vosk_model, self.sample_rate)

        self.console_manager.console_output(info_log="Settings: device={}, samplerate: {}".format(device_id, self.sample_rate))
        self.mic_stream = sd.RawInputStream(samplerate=self.sample_rate, device=device_id, blocksize = 8000, dtype='int16', channels=1,
                            callback=lambda indata, frames, time, status: self.callback(self, indata, frames, time, status))
        self.mic_stream.start()
        self.console_manager.console_output(info_log="Mic status: {}".format(self.mic_stream.active))
        
        self.console_manager.console_output(info_log="Microphone configured successfully!")
    
    def __exit__(self):
        self.mic_stream.close()
    
    @staticmethod
    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        # self.console_manager.console_output(info_log="Callback...")
        # print("callback...")
        if status:
            print("Callback status: %s" % status)
            # self.console_manager.console_output(info_log="Callback status: " + status)
        self.work_queue.put(bytes(indata))

    def recognize_input(self, already_activated=False):
        """
        Recognize input from mic and returns transcript if activation tag (assistant name) exist
        """

        while True:
            transcript = self._recognize_speech_from_mic()
            if already_activated or self._activation_name_exist(transcript):
                transcript = self._remove_activation_word(transcript)
                return transcript

    def _recognize_speech_from_mic(self, ):
        """
        Capture the words from the recorded audio (audio stream --> free text).
        Transcribe speech from recorded from `microphone`.
        """

        # self.console_manager.console_output(info_log="Get from queue")
        try:
            transcript = ''
            data = self.work_queue.get()
            # self.console_manager.console_output(info_log="Got data")
            if self.recognizer.AcceptWaveform(data):
                res = json.loads(self.recognizer.Result(), object_hook=lambda d: SimpleNamespace(**d))
                transcript = res.text
                self.console_manager.console_output(info_log='User said: {0}'.format(transcript))
                return transcript
            # else:
            #     # res = json.loads(self.recognizer.PartialResult(), object_hook=lambda d: SimpleNamespace(**d))
            #     # self.console_manager.console_output(info_log='Partial: {0}'.format(res.partial))
            #     print("Partial: " + self.recognizer.PartialResult())
        except queue.Empty:
            pass
            # print("Nothing detected yet")

    @staticmethod
    def _activation_name_exist(transcript):
        """
        Identifies the assistant name in the input transcript.
        """

        if transcript:
            transcript_words = transcript.split()
            return bool(set(transcript_words).intersection([jarvis.assistant_name]))
        else:
            return False

    @staticmethod
    def _remove_activation_word(transcript):
        transcript = transcript.replace(jarvis.assistant_name, '')
        return transcript
