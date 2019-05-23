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
        self.execute_state = {'ready_to_execute': False, 'enable_time': None}

    @log
    def execute_commands(self):


    def wake_up_check(self):
        """
        Checks if the state of the command manager (ready_to_execute)
        and if is not enabled search for enable word in user recorded speech.
        :return: boolean
        """
        if not self.execute_state['ready_to_execute']:
            if self._ready_to_execute_check:
                self._wake_up()
                return True
            else:
                return False
        else:
            return self._continue_listening()

    @log
    def shutdown_check(self):
        """
        Checks if there is the shutdown word,
        and if exists the assistant service stops.
        """
        # Check if a word from the triggering list exist in user words
        shutdown_tag = [triggering_word for triggering_word in
                            TRIGGERING_WORDS['disable_jarvis']['triggering_words']
                            if triggering_word in self.latest_voice_transcript]
        if shutdown_tag:
            assistant_response('Bye bye Sir. Have a nice day')
            logging.debug('Application terminated gracefully.')
            sys.exit()

    def _ready_to_execute_check(self):
        """
        Checks for enable tag and if exists return a boolean
        return: boolean
        """
        self._get_voice_transcript()
        enable_tag = [triggering_word for triggering_word in
                            TRIGGERING_WORDS['enable_jarvis']['triggering_words']
                            if triggering_word in self.latest_voice_transcript]
        return boolean(enable_tag)

    def _continue_listening(self):
        if datetime.now() > self.execute_state['enable_time'] + timedelta(seconds=10):
            self.execute_state = {'ready_to_execute': False,
                                  'enable_time': None}
            return False
        else:
            return True

    @staticmethod
    def _wake_up():
        """
        Creates the assistant respond according to the datetime hour and
        updates the execute state.
        """
        now = datetime.now()
        day_time = int(now.strftime('%H'))

        # Update command manager state, now the assistant is enabled!
        self.execute_state = {'ready_to_execute': True, 'enable_time': now}

        if day_time < 12:
            assistant_response('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            assistant_response('Hello Sir. Good afternoon')
        else:
            assistant_response('Hello Sir. Good evening')
        assistant_response('What do you want to do for you sir?')

    @log
    def _get_user_commands(self):
        """
        This method identifies the commands from the voice transcript
        and updates the commands state.
        e.x. latest_voice_transcript='open youtube and tell me the time'
        commands=[{'voice_transcript': 'open youtube and tell me the time',
                              'triggering_word': {'open'},
                              'command': open_website_in_browser},
                  {'voice_transcript': 'open youtube and tell me the time',
                    'triggering_word': {time'},
                    'command': tell_the_time},]
        """
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
    def _execute(self):
        """
        Execute one-by-one all the user commands and empty the
        queue with the waiting commands.
        """
        for command in self.commands:
            try:
                logging.debug('Execute the command {0}'.format(command))
                actions_mapping[command['command']](command['triggering_word'],
                command['voice_transcript'])
            except:
                logging.error('Error in command {0} excecution'.format(command))

            # Remove the executed or not command from the queue
            self.commands.remove(command)

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
        Capture the user speech and transform it to audio stream
        (speech --> audio stream).
        """
        with self.microphone as source:
            self.r.pause_threshold = SPEECH_RECOGNITION['pause_threshold']
            self.r.adjust_for_ambient_noise(source, duration=SPEECH_RECOGNITION['ambient_duration'])
            audio_text = self.r.listen(source)

        return audio_text
