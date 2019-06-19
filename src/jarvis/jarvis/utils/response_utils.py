import pyttsx3

from jarvis.utils.application_utils import OutputStyler
from jarvis.settings import GENERAL_SETTINGS
from jarvis.utils import application_utils


def set_voice_voice_engine():
    engine = pyttsx3.init()

    # Setting up new voice rate
    engine.setProperty('rate', 180)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 1.0)

    return engine


voice_engine = set_voice_voice_engine()


def assistant_response(text):
    """
    Assistant response in voice or/and in text.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_speech']:
        voice_engine.say(text)
        voice_engine.runAndWait()
        voice_engine.stop()

    if GENERAL_SETTINGS['response_in_text']:
        if GENERAL_SETTINGS['keep_only_last_response']:
            application_utils.clear()
            stdout_print(application_utils.jarvis_logo)
            stdout_print("  NOTE: CTRL + C If you want to Quit.")

        assistant_name = GENERAL_SETTINGS['assistant_name'] + ': '
        print(OutputStyler.HEADER + '='*48 + OutputStyler.ENDC)
        print(OutputStyler.HEADER + assistant_name + text + OutputStyler.ENDC)
        print(OutputStyler.HEADER + '='*48 + OutputStyler.ENDC)


def user_speech_playback(text):
    """
    Prints the user commands in text.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_text']:
        print(application_utils.user_input)


def stdout_print(text):
    """
    Application stdout with format.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_text']:
        print(OutputStyler.CYAN + text + OutputStyler.ENDC)