import sys
import logging
import speech_recognition as sr
from datetime import datetime

from jarvis.action_manager import ActionController
from jarvis.settings import TRIGGERING_WORDS, SPEECH_RECOGNITION
from jarvis.assistant_utils import assistant_response, user_speech_playback, log


class CommandController:
    commands_dict = {
        TRIGGERING_WORDS['open_browser']: ActionController.open_website_in_browser,
        TRIGGERING_WORDS['tell_time']: ActionController.tell_the_time,
        TRIGGERING_WORDS['tell_about']: ActionController.tell_me_about,
        TRIGGERING_WORDS['current_weather']: ActionController.tell_the_weather,
    }

    def __init__(self):
        self.microphone = sr.Microphone()
        self.r = sr.Recognizer()
        self.words = None

    def run(self):
        self.words = self._get_words()
        commands = self._get_commands()
        logging.debug('The {0} commands will be execute'.format(commands))
        self._execute_commands(commands)

    def wake_up_check(self):
        audio = self._record()
        try:
            self.words = self.r.recognize_google(audio).lower()
        except sr.UnknownValueError:
            self.words = self._get_words()

        if TRIGGERING_WORDS['enable_jarvis'] in self.words:
            self._wake_up_response()
            return True

    @log
    def shutdown_check(self):
        if TRIGGERING_WORDS['disable_jarvis'] in self.words:
            assistant_response('Bye bye Sir. Have a nice day')
            sys.exit()

    @staticmethod
    def _wake_up_response():
        now = datetime.now()
        day_time = int(now.strftime('%H'))
        if day_time < 12:
            assistant_response('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            assistant_response('Hello Sir. Good afternoon')
        else:
            assistant_response('Hello Sir. Good evening')
        assistant_response('What do you want to do for you sir?')

    def _execute_commands(self, commands):
        if bool(commands):
            for command in commands:
                logging.debug('Execute the command {0}'.format(command))
                self.commands_dict[command](self.words)
        else:
            assistant_response('Sorry, no commands to execute')

    def _get_commands(self):
        words = self.words.split()
        commands_set = set(self.commands_dict.keys())
        words_set = set(words)
        return commands_set.intersection(words_set)

    def _get_words(self):
        audio = self._record()
        try:
            recognized_words = self.r.recognize_google(audio).lower()
            logging.debug('Recognized words: ' + recognized_words)
            user_speech_playback(recognized_words)
        except sr.UnknownValueError:
            assistant_response('....')
            recognized_words = self._get_words()
        return recognized_words

    def _record(self):
        with self.microphone as source:
            self.r.pause_threshold = SPEECH_RECOGNITION['pause_threshold']
            self.r.adjust_for_ambient_noise(source, duration=SPEECH_RECOGNITION['ambient_duration'])
            audio_text = self.r.listen(source)
        return audio_text
