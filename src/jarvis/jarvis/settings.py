
# General assistant settings
GENERAL_SETTINGS = {
    'assistant_name': 'Jarvis',
    'response_in_speech': False,
    'response_in_text': True
}

# Trigger words
TRIGGERING_WORDS = {
    'enable_jarvis': 'start',
    'disable_jarvis': 'stop',
    'open_browser': 'open',
    'sent_email': 'email',
    'launch_application': 'launch',
    'tell_time': 'time',
    'tell_about': 'about',
    'current_weather': 'weather'
}

# Google API Speech recognition settings
# SpeechRecognition: https://pypi.org/project/SpeechRecognition/2.1.3
SPEECH_RECOGNITION = {
    'ambient_duration': 0.1,
    'pause_threshold': 1,  # minimum length silence (in seconds) at the end of a sentence
    'energy_threshold': 4000,  # microphone sensitivity, for loud places, the energy level should be up to 4000
    'dynamic_energy_threshold': False  # For unpredictable noise levels
}

# Google text to speech API settings
GOOGLE_SPEECH = {
    'lang': "en"
}

# Open weather map API conf settings
WEATHER_API = {
    'unit': 'celsius',
    'key': '2e63db2f8df7cc9ebd13a441d8b2eb8a'
}
