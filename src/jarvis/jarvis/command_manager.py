import sys
import logging
import speech_recognition as sr
from datetime import datetime

from jarvis.action_manager import actions_mapping
from jarvis.settings import TRIGGERING_WORDS, SPEECH_RECOGNITION
from jarvis.assistant_utils import assistant_response, user_speech_playback, log


class CommandManager:

    def __init__(self):
        self.microphone = sr.Microphone()
        self.r = sr.Recognizer()
        self.commands = []
        self.latest_voice_transcript = ''

    @log
    def run(self):
        self._get_voice_transcript()
        self._get_user_commands()
        self._execute_commands()

    def wake_up_check(self):
        """
        Checks if there is the enable word in user speech.
        :return: boolean
        """
        self._get_voice_transcript()
        triggering_words = [triggering_word for triggering_word in
                            TRIGGERING_WORDS['enable_jarvis']['triggering_words']
                            if triggering_word in self.latest_voice_transcript]
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
                            TRIGGERING_WORDS['disable_jarvis']['triggering_words']
                            if triggering_word in self.latest_voice_transcript]
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

    @log
    def _get_user_commands(self):
        for triggering_words in TRIGGERING_WORDS.values():
            for triggering_word in triggering_words['triggering_words']:
                if triggering_word in self.latest_voice_transcript:
                    command = triggering_words['command']
                    exist_command = actions_mapping.get(command)
                    if exist_command:
                        self.commands.append({'voice_transcript': self.latest_voice_transcript,
                                              'triggering_word': triggering_word,
                                              'command': command})

    @log
    def _execute_commands(self):
        """
        Execute user commands. Checks one-by-one all the triggering _get_voice_transcript
        and if a triggering word exist in user words then it executes the
        corresponding command.
        """
        for command in self.commands:
            logging.debug('Execute the command {0}'.format(command))
            actions_mapping[command['command']](command['triggering_word'], command['voice_transcript'])

    def _get_voice_transcript(self):
        """
        Capture the words from the recorded audio (audio stream --> free text).
        """
        audio = self._record()
        try:
            self.latest_voice_transcript = self.r.recognize_google(audio).lower()
            logging.debug('Recognized words: ' + self.latest_voice_transcript)
            user_speech_playback(self.latest_voice_transcript)
        except sr.UnknownValueError:
            assistant_response('....')
            self.latest_voice_transcript = self._get_voice_transcript()

        return self.latest_voice_transcript

    def _record(self):
        """
        Capture the user speech and transform it to audio stream (speech --> audio stream).
        """
        with self.microphone as source:
            self.r.pause_threshold = SPEECH_RECOGNITION['pause_threshold']
            self.r.adjust_for_ambient_noise(source, duration=SPEECH_RECOGNITION['ambient_duration'])
            audio_text = self.r.listen(source)

        return audio_text
