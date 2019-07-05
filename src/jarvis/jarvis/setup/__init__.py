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

import speech_recognition as sr
import pyttsx3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from jarvis.utils.application_utils import clear
from jarvis.settings import SPEECH_RECOGNITION
from jarvis.engines.tts import TTSEngine
from jarvis.engines.stt import STTEngine
from jarvis.core.analyzer import Analyzer
from jarvis.settings import GENERAL_SETTINGS


def set_microphone(r):
    """
    Setup the assistant microphone.
    """
    microphone_list = sr.Microphone.list_microphone_names()

    clear()
    print("=" * 48)
    print("Microphone Setup")
    print("=" * 48)
    print("Which microphone do you want to use a assistant mic:")

    for index, name in enumerate(microphone_list):
        print("{0}) Microphone: {1}".format(index, name))

    choices = "Choice[1-{0}]: ".format(len(microphone_list))
    print("WARNING: In case of error of 'Invalid number of channels' try again with different micrphone choice")
    index = input(choices)

    while not index.isnumeric():
        index = input('Please select a number between choices[1-{0}]: '.format(len(microphone_list)))

    with sr.Microphone(device_index=int(index), chunk_size=512) as source:
        r.pause_threshold = SPEECH_RECOGNITION['pause_threshold']
        r.energy_threshold = SPEECH_RECOGNITION['energy_threshold']

        clear()
        print("-" * 48)
        print("Microphone Calibration")
        print("-" * 48)

        print("Please wait.. for {} seconds ".format(SPEECH_RECOGNITION['ambient_duration']))
        r.adjust_for_ambient_noise(source, duration=SPEECH_RECOGNITION['ambient_duration'])
        r.dynamic_energy_threshold = SPEECH_RECOGNITION['dynamic_energy_threshold']
        print("Microphone calibrated successfully!")

        return source




def set_voice_engine():
    """
    Setup text to speech engine
    :return: gtts engine object
    """
    tts_engine = pyttsx3.init()

    # Setting up new voice rate
    tts_engine.setProperty('rate', 160)

    # Setting up volume level  between 0 and 1
    tts_engine.setProperty('volume', 1.0)

    return tts_engine

engine = set_voice_engine()
tts_engine = TTSEngine(engine_=engine,
                       speech_response_enabled=GENERAL_SETTINGS['response_in_speech']
                       )




if GENERAL_SETTINGS['user_voice_input']:
    recognizer = sr.Recognizer()
    microphone = set_microphone(recognizer)
else:
    recognizer = None
    microphone = None
stt_engine = STTEngine(speech_recognizer=recognizer,
                       microphone=microphone)


args = {
    "stop_words": "english",
    "lowercase": True,
    "norm": 'l1',
    "use_idf": True,
}

analyzer = Analyzer(weight_measure=TfidfVectorizer,
                         similarity_measure=cosine_similarity,
                         args=args,
                         skills_=SKILLS
                         )
