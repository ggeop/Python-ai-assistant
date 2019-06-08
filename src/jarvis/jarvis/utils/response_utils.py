from google_speech import Speech

from jarvis.utils.application_utils import OutputStyler
from jarvis.settings import GOOGLE_SPEECH, GENERAL_SETTINGS


def assistant_response(text):
    """
    Assistant response in voice or/and in text.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_speech']:
        speech = Speech(text, GOOGLE_SPEECH['lang'])
        speech.play()
    if GENERAL_SETTINGS['response_in_text']:
        assistant_name = GENERAL_SETTINGS['assistant_name'] + ': '
        print('-'*48)
        print(assistant_name + OutputStyler.CYAN + text + OutputStyler.ENDC)
        print('-'*48 + '\n')


def user_speech_playback(text):
    """
    Prints the user commands in voice or/and in text.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_speech']:
        speech = Speech(text, GOOGLE_SPEECH['lang'])
        speech.play()
    if GENERAL_SETTINGS['response_in_text']:
        print('-' * 48)
        print('You: ' + OutputStyler.CYAN + text + OutputStyler.ENDC)
        print('-'*48 + '\n')


def stdout_print(text):
    """
    Application stdout with format.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_text']:
        print(OutputStyler.CYAN + text + OutputStyler.ENDC)