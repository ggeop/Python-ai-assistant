import sys
import logging
import speech_recognition as sr
from datetime import datetime

from jarvis.settings import SPEECH_RECOGNITION
from jarvis.assistant_utils import assistant_response, user_speech_playback, log
from jarvis.actions_registry import ACTIONS

class ActionController:
    def __init__(self):
        self.microphone = sr.Microphone()
        self.r = sr.Recognizer()
        self.actions = []
        self.latest_voice_transcript = ''
        self.execute_state = {'ready_to_execute': False, 'enable_time': None}

    def wake_up_check(self):
        """
        Checks if the state of the action manager (ready_to_execute)
        and if is not enabled search for enable word in user recorded speech.
        :return: boolean
        """
        if not self.execute_state['ready_to_execute']:
            if self._ready_to_execute_check:
                self.execute_state = actions_mapping['enable_jarvis']['action']
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
        shutdown_tag = [tag for tag in ACTIONS['disable_jarvis']['tags']
                            if tag in self.latest_voice_transcript]
        if shutdown_tag:
            actions_mapping['disable_jarvis']['action']


    def _ready_to_execute_check(self):
        """
        Checks for enable tag and if exists return a boolean
        return: boolean
        """
        self._get_voice_transcript()
        enable_tag = [tag for tag in ACTIONS['enable_jarvis']['tags']
                          if tag in self.latest_voice_transcript]
        return boolean(enable_tag)

    def _continue_listening(self):
        # TODO: Add to settings the waiting number of seconds
        if datetime.now() > self.execute_state['enable_time'] + timedelta(seconds=10):
            self.execute_state = {'ready_to_execute': False,
                                  'enable_time': None}
            return False
        else:
            return True

    @log
    def _get_user_actions(self):
        """
        This method identifies the actions from the voice transcript
        and updates the actions state.
        e.x. latest_voice_transcript='open youtube and tell me the time'
        actions=[{'voice_transcript': 'open youtube and tell me the time',
                    'tag': {'open'},
                    'action': open_website_in_browser},
                  {'voice_transcript': 'open youtube and tell me the time',
                    'tag': {time'},
                    'action': tell_the_time},
                    ]
        """
        for tags in ACTIONS.values():
            for tag in tags['tag']:
                if tag in self.latest_voice_transcript:
                    self.actions.append({'voice_transcript': self.latest_voice_transcript,
                                          'tag': tag,
                                           'action': tag['action']})

    @log
    def _execute(self):
        """
        Execute one-by-one all the user actions and empty the
        queue with the waiting actions.
        """
        for action in self.actions:
            try:
                logging.debug('Execute the action {0}'.format(action))
                ACTIONS[action['action']](action['tag'], action['voice_transcript'])
            except:
                logging.error('Error in action {0} excecution'.format(action))

            # Remove the executed or not action from the queue
            self.actions.remove(action)

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
