import speech_recognition as sr
import pyttsx3

from jarvis.utils.application_utils import clear
from jarvis.settings import SPEECH_RECOGNITION


def set_microphone(r):
    """
    Setup the assistant microphone.
    """
    microphone_list = sr.Microphone.list_microphone_names()

    clear()
    print("=" * 48)
    print("Microphone Setup")
    print("=" * 48)
    print("Which microphone do you want to use a assistant mic:")

    for index, name in enumerate(microphone_list):
        print("{0}) Microphone: {1}".format(index, name))

    choices = "Choice[1-{0}]: ".format(len(microphone_list))
    print("WARNING: In case of error of 'Invalid number of channels' try again with different micrphone choice")
    index = input(choices)

    while not index.isnumeric():
        index = input('Please select a number between choices[1-{0}]: '.format(len(microphone_list)))

    with sr.Microphone(device_index=int(index), chunk_size=512) as source:
        r.pause_threshold = SPEECH_RECOGNITION['pause_threshold']
        r.energy_threshold = SPEECH_RECOGNITION['energy_threshold']
        print("Please wait.. for {} seconds ".format(SPEECH_RECOGNITION['ambient_duration']))
        print("Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=SPEECH_RECOGNITION['ambient_duration'])
        r.dynamic_energy_threshold = SPEECH_RECOGNITION['dynamic_energy_threshold']

        return source


def set_voice_engine():
    engine = pyttsx3.init()

    # Setting up new voice rate
    engine.setProperty('rate', 160)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 1.0)

    return engine
