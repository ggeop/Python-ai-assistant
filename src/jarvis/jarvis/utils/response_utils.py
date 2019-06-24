import threading

from jarvis.utils.application_utils import OutputStyler
from jarvis.settings import GENERAL_SETTINGS
from jarvis.utils import application_utils
from jarvis.setup import set_voice_engine


engine = set_voice_engine()


def create_text_batches(raw_text, number_of_words_per_batch=5):
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
    """
    Speech method translate text batches to speech
    :param text: string (e.g 'tell me about google')
    """

    batches = create_text_batches(raw_text=text)

    cumulative_batch = ''
    for batch in batches:
        engine.say(batch)
        cumulative_batch += batch
        print_assistant_response(cumulative_batch)
        try:
            engine.runAndWait()
        except RuntimeError:
            pass
        if application_utils.stop_speaking:
            break


def print_assistant_response(text):
    application_utils.clear()
    stdout_print(application_utils.jarvis_logo)
    stdout_print("  NOTE: CTRL + C If you want to Quit.")
    print(OutputStyler.BOLD +
          '  MIC INFO: ENERGY THRESHOLD LEVEL: ' + '|'*int(application_utils.energy_threshold) + '\n'
          '              DYNAMIC ENERGY LEVEL: ' + '|'*int(application_utils.dynamic_energy_ratio) + OutputStyler.ENDC)
    assistant_name = GENERAL_SETTINGS['assistant_name'] + ': '
    print(OutputStyler.HEADER + '=' * 48 + OutputStyler.ENDC)
    print(OutputStyler.HEADER + assistant_name + text + '\r' + OutputStyler.ENDC)
    print(OutputStyler.HEADER + '=' * 48 + OutputStyler.ENDC)


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
    else:
        print_assistant_response(text)


def user_speech_playback(text):
    """
    Prints the user commands in text.
    :param text: string
    """
    print(application_utils.user_input)


def stdout_print(text):
    """
    Application stdout with format.
    :param text: string
    """
    print(OutputStyler.CYAN + text + OutputStyler.ENDC)