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

LOG_SETTINGS = {
    'version': 1,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': '/var/log/jarvis.log',
            'mode': 'a',
            'maxBytes': 10000000,
            'backupCount': 3,
        },
    },
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    }
}

# General assistant settings
GENERAL_SETTINGS = {
    'assistant_name': 'Jarvis',
    'enable_period': 300,  # In seconds
    'user_voice_input': False,  # True: The assistant responds in voice commands,
                                # False: The assistant waiting for text input
    'response_in_speech': True,
}

# Google API Speech recognition settings
# SpeechRecognition: https://pypi.org/project/SpeechRecognition/2.1.3
SPEECH_RECOGNITION = {
    'ambient_duration': 1,  # Time for auto microphone calibration
    'pause_threshold': 1,  # minimum length silence (in seconds) at the end of a sentence
    'energy_threshold': 3000,  # microphone sensitivity, for loud places, the energy level should be up to 4000
    'dynamic_energy_threshold': True  # For unpredictable noise levels (Suggested to be TRUE)
}

# Google text to speech API settings
GOOGLE_SPEECH = {
    'lang': "en"
}


# Open weather map API settings
# Create key: https://openweathermap.org/appid
WEATHER_API = {
    'unit': 'celsius',
    'key': '2e63db2f8df7cc9ebd13a441d8b2eb8a'
}

# WolframAlpha API settings
# Create key: https://developer.wolframalpha.com/portal/myapps/
WOLFRAMALPHA_API = {
    'key': 'WW4JAY-VR7EAAPXJ5'
}

# IPSTACK API settings
#Create key: https://ipstack.com/signup/free
IPSTACK_API = {
    'key': 'bff2692443af80b42129323e2101fa60'
}
