import threading

from jarvis.utils.application_utils import OutputStyler
from jarvis.settings import GENERAL_SETTINGS
from jarvis.utils import application_utils
from jarvis.setup import set_voice_engine


engine = set_voice_engine()


def create_text_batches(raw_text, number_of_words_per_batch = 10):
    """
    Splits the user speech into batches and return a list with the split batches
    :param raw_text: string
    :param number_of_words_per_batch: int
    :return: list
    """

    raw_text = raw_text + ' '
    list_of_batches = []
    total_words = raw_text.count(' ')
    letter_id = 0

    for split in range(0, int(total_words / number_of_words_per_batch)):
        batch = ''
        words_count = 0
        while words_count < number_of_words_per_batch:
            batch += raw_text[letter_id]
            if raw_text[letter_id] == ' ':
                words_count += 1
            letter_id += 1
        list_of_batches.append(batch)

    # Add the rest of word in a batch
    if letter_id < len(raw_text):
        list_of_batches.append(raw_text[letter_id:])
    return list_of_batches


def speech(text):

    batches = create_text_batches(raw_text=text)

    for batch in batches:
        engine.say(batch)
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