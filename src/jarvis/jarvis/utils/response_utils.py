from google_speech import Speech

from jarvis.utils.application_utils import OutputStyler
from jarvis.settings import GOOGLE_SPEECH, GENERAL_SETTINGS
from jarvis.utils import application_utils


def assistant_response(text):
    """
    Assistant response in voice or/and in text.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_speech']:
        speech = Speech(text, GOOGLE_SPEECH['lang'])
        speech.play()
    if GENERAL_SETTINGS['response_in_text']:
        application_utils.clear()
        stdout_print(application_utils.jarvis_logo)
        stdout_print("  NOTE: CTRL + C If you want to Quit.")
        assistant_name = GENERAL_SETTINGS['assistant_name'] + ': '
        print(OutputStyler.HEADER + '='*48 + OutputStyler.ENDC)
        print(OutputStyler.HEADER + assistant_name + text + OutputStyler.ENDC)
        print(OutputStyler.HEADER + '=' * 48 + OutputStyler.ENDC)


def user_speech_playback(text):
    """
    Prints the user commands in voice or/and in text.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_speech']:
        speech = Speech(text, GOOGLE_SPEECH['lang'])
        speech.play()
    if GENERAL_SETTINGS['response_in_text']:
        print(application_utils.user_input)


def stdout_print(text):
    """
    Application stdout with format.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_text']:
        print(OutputStyler.CYAN + text + OutputStyler.ENDC)