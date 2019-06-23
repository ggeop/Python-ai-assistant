import threading

from jarvis.utils.application_utils import OutputStyler
from jarvis.settings import GENERAL_SETTINGS
from jarvis.utils import application_utils
from jarvis.setup import set_voice_engine


engine = set_voice_engine()


def speech(text):
    words = text.split()
    for word in words:
        engine.say(word)
        try:
            engine.runAndWait()
        except RuntimeError:
            pass
        if application_utils.stop_speaking:
            break


def assistant_response(text):
    """
    Assistant response in voice or/and in text.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_speech']:

        application_utils.stop_speaking = False
        try:
            t1 = threading.Thread(target=speech, args=[text])
            t1.start()
        except RuntimeError:
            pass

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