import threading
import subprocess

from jarvis.utils.application_utils import OutputStyler
from jarvis.settings import GENERAL_SETTINGS
from jarvis.utils import application_utils
from jarvis.setup import set_voice_engine
from jarvis.core import controller
from jarvis.skills import system_health_skills
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
        if controller.State.stop_speaking:
            controller.State.stop_speaking = False
            break

def print_assistant_response(text):
    application_utils.clear()

    stdout_print(application_utils.jarvis_logo)

    stdout_print("  NOTE: CTRL + C If you want to Quit.")

    print(OutputStyler.HEADER + '-------------- INFO --------------' + OutputStyler.ENDC)

    print(OutputStyler.HEADER + 'SYSTEM ---------------------------' + OutputStyler.ENDC)
    print(OutputStyler.BOLD +
          'RAM USAGE: {0:.2f} GB'.format(system_health_skills.get_memory_consumption()) + OutputStyler.ENDC)

    print(OutputStyler.HEADER + 'MIC ------------------------------' + OutputStyler.ENDC)
    print(OutputStyler.BOLD +
          'ENERGY THRESHOLD LEVEL: ' + '|'*int(controller.State.energy_threshold) + '\n'
          'DYNAMIC ENERGY LEVEL: ' + '|'*int(controller.State.dynamic_energy_ratio) + OutputStyler.ENDC)
    print(' ')

    print(OutputStyler.HEADER + '-------------- LOG --------------' + OutputStyler.ENDC)
    lines = subprocess.check_output(['tail', '-10', '/var/log/jarvis.log']).decode("utf-8")
    print(OutputStyler.BOLD + lines + OutputStyler.ENDC)

    print(OutputStyler.HEADER + '-------------- ASSISTANT --------------' + OutputStyler.ENDC)
    print(OutputStyler.BOLD + '  > ' + text + '\r' + OutputStyler.ENDC)


def assistant_response(text):
    """
    Assistant response in voice or/and in text.
    :param text: string
    """
    if GENERAL_SETTINGS['response_in_speech']:
        application_utils.stop_speaking = False
        try:
            speech_tread = threading.Thread(target=speech, args=[text])
            speech_tread.start()
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