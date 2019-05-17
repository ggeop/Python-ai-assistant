import speech_recognition as sr
import logging

from jarvis.action_controller import ActionController
from jarvis.settings import TRIGGERING_WORDS, SPEECH_RECOGNITION
from jarvis.assistant_utils import CommandWords


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
        commands = self._get_commands(self.words)
        self._execute_commands(commands, self.words)

    def wake_up(self):
        audio = self._listen()
        try:
            self.words = self.r.recognize_google(audio).lower()
        except sr.UnknownValueError:
            self.words = self._get_words()

        if CommandWords.hello in self.words:
            self._wake_up_response()
            self.words = None
            return True

    def shutdown(self):
        if CommandWords.shutdown in self.words:
            assistant_response('Bye bye Sir. Have a nice day')
            sys.exit()

    def _wake_up_response(self):
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
                logging.info('Execute the command {0}'.format(command))
                cls.commands_dict[command](self.words)
        else:
            logging.info('Sorry, no commands to execute')

    def _get_commands(self):
        words = self.words.split()
        commands_set = set(commands_dict.keys())
        words_set = set(words)
        return commands_set.intersection(words_set)

    def _get_words(self):
        audio = self._listen()
        try:
            recognized_words = self.r.recognize_google(audio).lower()
            print('You said: ' + recognized_words + '\n')
        except sr.UnknownValueError:
            print('....')
            recognized_words = self._get_words()
        return recognized_words

    def _listen(self):
        with self.microphone as source:
            self.r.pause_threshold = SPEECH_RECOGNITION['pause_treshold']
            self.r.adjust_for_ambient_noise(source, duration=SPEECH_RECOGNITION['ambient_duration'])
            audio_text = self.r._listen(source)
        return audio_text
