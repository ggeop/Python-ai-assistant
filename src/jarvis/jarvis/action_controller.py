import logging
import speech_recognition as sr
from datetime import datetime, timedelta

from jarvis.settings import GENERAL_SETTINGS, SPEECH_RECOGNITION
from jarvis.assistant_utils import assistant_response, user_speech_playback, log
from jarvis.actions_registry import ACTIONS, CONTROL_ACTIONS


class ActionController:
    def __init__(self):
        self.microphone = sr.Microphone()
        self.r = sr.Recognizer()
        self.actions_to_execute = []
        self.latest_voice_transcript = ''
        self.execute_state = {'ready_to_execute': False, 'enable_time': None}

    def wake_up_check(self):
        """
        Checks if the state of the action manager (ready_to_execute)
        and if is not enabled search for enable word in user recorded speech.
        :return: boolean
        """
        if not self.execute_state['ready_to_execute']:
            return self._ready_to_start()
        else:
            return self._continue_listening()

    @log
    def shutdown_check(self):
        """
        Checks if there is the shutdown word, and if exists the assistant service stops.
        """
        transcript_words = self.latest_voice_transcript.split()
        shutdown_tag = set(transcript_words).intersection(CONTROL_ACTIONS['disable_jarvis']['tags'])

        if bool(shutdown_tag):
            CONTROL_ACTIONS['disable_jarvis']['action']()

    def _ready_to_start(self):
        """
        Checks for enable tag and if exists return a boolean
        return: boolean
        """
        self._get_voice_transcript()

        transcript_words = self.latest_voice_transcript.split()
        enable_tag = set(transcript_words).intersection(CONTROL_ACTIONS['enable_jarvis']['tags'])

        if bool(enable_tag):
            self.execute_state = CONTROL_ACTIONS['enable_jarvis']['action']()
            return True

    def _continue_listening(self):
        """
        Checks if the assistant enable time (triggering time + enable period) has passed.
        return: boolean
        """
        if datetime.now() > self.execute_state['enable_time'] + timedelta(seconds=GENERAL_SETTINGS['enable_period']):
            self.execute_state = {'ready_to_execute': False,
                                  'enable_time': None}
            return False
        else:
            return True

    @log
    def _get_user_actions(self):
        """
        This method identifies the active actions from the voice transcript
        and updates the actions state.

        e.x. latest_voice_transcript='open youtube'
        Then, the actions_to_execute will be the following:
        actions_to_execute=[{voice_transcript': 'open youtube',
                             'tag': 'open',
                             'action': ActionManager.open_website_in_browser
                            ]
        """
        for action in ACTIONS.values():
            if action['enable']:
                for tag in action['tags']:
                    if tag in self.latest_voice_transcript:
                        action = {'voice_transcript': self.latest_voice_transcript,
                                  'tag': tag,
                                  'action': action['action']}

                        logging.debug('Update actions queue with action: {0}'.format(action))
                        self.actions_to_execute.append(action)

    def _execute(self):
        """
        Execute one-by-one all the user actions and empty the queue with the waiting actions.
        """
        for action in self.actions_to_execute:
            if action['tag'] in CONTROL_ACTIONS['enable_jarvis']['tags']:
                assistant_response(" I don't sleep !")
            else:
                logging.debug('Execute the action {0}'.format(action))
                action['action'](**action)

            # Remove the executed or not action from the queue
            self.actions_to_execute.remove(action)

    def _get_voice_transcript(self):
        """
        Capture the words from the recorded audio (audio stream --> free text).
        """
        # audio = self._record()
        # try:
        #     self.latest_voice_transcript = self.r.recognize_google(audio).lower()
        #     logging.debug('Recognized words: ' + self.latest_voice_transcript)
        #     user_speech_playback(self.latest_voice_transcript)
        # except sr.UnknownValueError:
        #     assistant_response('....')
        #     self.latest_voice_transcript = self._get_voice_transcript()
        self.latest_voice_transcript=input('user input: ')
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
