import sys
import logging
import speech_recognition as sr
from datetime import datetime

from jarvis.action_manager import ActionManager
from jarvis.settings import TRIGGERING_WORDS, SPEECH_RECOGNITION
from jarvis.assistant_utils import assistant_response, user_speech_playback, log


class CommandManager:
    commands_dict = {
        TRIGGERING_WORDS['open_browser']['command']: ActionManager.open_website_in_browser,
        TRIGGERING_WORDS['tell_time']['command']: ActionManager.tell_the_time,
        TRIGGERING_WORDS['tell_about']['command']: ActionManager.tell_me_about,
        TRIGGERING_WORDS['current_weather']['command']: ActionManager.tell_the_weather,
        TRIGGERING_WORDS['disable_jarvis']['command']: ActionManager.disable_jarvis,
    }

    def __init__(self):
        self.microphone = sr.Microphone()
        self.r = sr.Recognizer()
        self.words = None

    @log
    def run(self):
        self.words = self._get_words()
        self._execute_commands(commands)

    def wake_up_check(self):
        """
        Checks if there is the enable word in user speech.
        :return: boolean
        """
        audio = self._record()
        try:
            self.words = self.r.recognize_google(audio).lower()
        except sr.UnknownValueError:
            self.words = self._get_words()
        # Check if a word from the triggering list exist in user words
        triggering_words = [triggering_word for triggering_word in
                            TRIGGERING_WORDS['enable_jarvis']['triggering_words']if triggering_word in self.words]
        if triggering_words:
            self._wake_up_response()
            return True
        else:
            return False

    @log
    def shutdown_check(self):
        """
        Checks if there is the shutdown word, and if exists the assistant service stops.
        """
        # Check if a word from the triggering list exist in user words
        triggering_words = [triggering_word for triggering_word in
                            TRIGGERING_WORDS['disable_jarvis']['triggering_words'] if triggering_word in self.words]
        if triggering_words:
            assistant_response('Bye bye Sir. Have a nice day')
            logging.debug('Application terminated gracefully.')
            sys.exit()

    @staticmethod
    def _wake_up_response():
        """
        Creates the assistant respond according to the datetime hour.
        """
        now = datetime.now()
        day_time = int(now.strftime('%H'))
        if day_time < 12:
            assistant_response('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            assistant_response('Hello Sir. Good afternoon')
        else:
            assistant_response('Hello Sir. Good evening')
        assistant_response('What do you want to do for you sir?')

    def _execute_commands(self):
        """
        Execute user commands. Checks one-by-one all the triggering _get_words
        and if a triggering word exist in user words then it executes the
        corresponding command.
        e.x.
        self.words ='open youtube and tell me the time'
        words =['open', 'youtube', 'and', 'tell', 'me', 'the', 'time']
        The application runs the following:
         execute--> open_website_in_browser('open', self.words)
         execute--> tell_the_time('time', self.words)

        NOTE: If the same triggering command exists more than once the Application
        execute the command once.
        e.x.
            words =['open', 'youtube', 'and', 'open', 'netflix']
            The application will run only once the open_website_in_browser.
             execute--> open_website_in_browser('open', self.words)

        """
        words = self.words.split()
        for triggering_words in TRIGGERING_WORDS.values():
             for triggering_word in triggering_words['triggering_words']:
                 if triggering_word in words:
                     command = triggering_words['command']
                     exist_command = self.commands_dict.get(command)
                     if exist_command:
                         logging.debug('Execute the command {0}'.format(command))
                         self.commands_dict[command](triggering_word, self.words)
                     else:
                         logging.debug('Not command {0} to execute'.format(command))

    def _get_words(self):
        """
        Capture the words from the recorded audio (audio stream --> free text).
        """
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
        """
        Capture the user speech and transform it to audio stream (speech --> audio stream).
        """
        with self.microphone as source:
            self.r.pause_threshold = SPEECH_RECOGNITION['pause_threshold']
            self.r.adjust_for_ambient_noise(source, duration=SPEECH_RECOGNITION['ambient_duration'])
            audio_text = self.r.listen(source)

        return audio_text
