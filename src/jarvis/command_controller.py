import speech_recognition as sr
import logging

from jarvis.action_controller import ActionController
from jarvis.settings import *

commands_dict = {BROWSER_TRIGGERING_WORD: ActionController.open_website_in_browser,
                 TELL_TIME: ActionController.tell_the_time,
                 TELL_ME_ABOUT: ActionController.tell_me_about
                 }


class CommandController:

    @classmethod
    def execute_commands(cls, commands, words):
        if bool(commands):
            for command in commands:
                logging.info('Execute the command {0}'.format(command))
                commands_dict[command](words)
        else:
            logging.info('Sorry, no commands to execute')

    @classmethod
    def get_commands(cls, words):
        words = words.split()
        commands_set = set(commands_dict.keys())
        words_set = set(words)
        return commands_set.intersection(words_set)

    @classmethod
    def get_words(cls):
        r = sr.Recognizer()
        audio = cls.listen(r)
        try:
            words = r.recognize_google(audio).lower()
            print('You said: ' + words + '\n')
            words = words
        except sr.UnknownValueError:
            print('....')
            words = cls.get_words()
        return words

    @classmethod
    def listen(cls, r):
        with sr.Microphone() as source:
            r.pause_threshold = PAUSE_THESHOLD
            r.adjust_for_ambient_noise(source, duration=AMBIENT_DURATION)
            audio_text = r.listen(source)
        return audio_text
