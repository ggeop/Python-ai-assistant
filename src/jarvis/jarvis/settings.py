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
    'enable_period': 190,  # In seconds
    'user_voice_input': True,  # True: The assistant responds in voice commands,
                                # False: The assistant waiting for text input
    'response_in_speech': True,
}

# Google API Speech recognition settings
# SpeechRecognition: https://pypi.org/project/SpeechRecognition/2.1.3
SPEECH_RECOGNITION = {
    'ambient_duration': 4,  # Time for auto microphone calibration
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
    'key': None
}

# WolframAlpha API settings
# Create key: https://developer.wolframalpha.com/portal/myapps/
WOLFRAMALPHA_API = {
    'key': None
}

# IPSTACK API settings
#Create key: https://ipstack.com/signup/free
IPSTACK_API = {
    'key': None
}
