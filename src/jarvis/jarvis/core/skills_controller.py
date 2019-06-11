import logging
import speech_recognition as sr
from datetime import datetime, timedelta

from jarvis.settings import GENERAL_SETTINGS, SPEECH_RECOGNITION
from jarvis.utils.response_utils import assistant_response, user_speech_playback
from jarvis.utils.application_utils import log, clear
from jarvis.skills.skills_registry import BASIC_SKILLS, CONTROL_SKILLS


class ControllerUtils:
    def __init__(self):
        self.microphone = self._set_microphone()
        self.r = sr.Recognizer()
        self.skills_to_execute = []
        self.latest_voice_transcript = ''
        self.execute_state = {'ready_to_execute': False, 'enable_time': None}

    def wake_up_check(self):
        """
        Checks if the state of the skill manager (ready_to_execute)
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
        shutdown_tag = set(transcript_words).intersection(CONTROL_SKILLS['disable_jarvis']['tags'])

        if bool(shutdown_tag):
            CONTROL_SKILLS['disable_jarvis']['skill']()

    def get_transcript(self):
        """
        Capture the words from the recorded audio (audio stream --> free text).
        """
        if GENERAL_SETTINGS['user_voice_input']:
            audio = self._record()
            self._recognize_voice(audio)
        else:
            self.latest_voice_transcript = input('You: ')
            while self.latest_voice_transcript == '':
                assistant_response("Say something..")
                self.latest_voice_transcript = input('You: ')
        return self.latest_voice_transcript

    @staticmethod
    def _set_microphone():
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
            return source

    def _ready_to_start(self):
        """
        Checks for enable tag and if exists return a boolean
        return: boolean
        """
        self.get_transcript()

        transcript_words = self.latest_voice_transcript.split()
        enable_tag = set(transcript_words).intersection(CONTROL_SKILLS['enable_jarvis']['tags'])

        if bool(enable_tag):
            self.execute_state = CONTROL_SKILLS['enable_jarvis']['skill']()
            return True

    def _continue_listening(self):
        """
        Checks if the assistant enable time (triggering time + enable period) has passed.
        return: boolean
        """
        if datetime.now() > self.execute_state['enable_time'] + timedelta(seconds=GENERAL_SETTINGS['enable_period']):
            self.execute_state = {'ready_to_execute': False,
                                  'enable_time': None}

            assistant_response("Time passed.. I go to sleep..")
            return False
        else:
            return True

    def _recognize_voice(self, audio):
        try:
            self.latest_voice_transcript = self.r.recognize_google(audio).lower()
            logging.debug('Recognized words: ' + self.latest_voice_transcript)
            user_speech_playback(self.latest_voice_transcript)
        except sr.UnknownValueError:
            assistant_response('....')
        except sr.RequestError:
            assistant_response("Try later.. (Google API was unreachable..)")

    def _record(self):
        """
        Capture the user speech and transform it to audio stream (speech --> audio stream).
        """
        with self.microphone as source:
            self.r.pause_threshold = SPEECH_RECOGNITION['pause_threshold']
            self.r.adjust_for_ambient_noise(source, duration=SPEECH_RECOGNITION['ambient_duration'])
            audio_text = self.r.listen(source)

        return audio_text


class SkillsController(ControllerUtils):

    @log
    def get_skills(self):
        """
        This method identifies the active skills from the voice transcript
        and updates the skills state.

        e.x. latest_voice_transcript='open youtube'
        Then, the skills_to_execute will be the following:
        skills_to_execute=[{voice_transcript': 'open youtube',
                             'tag': 'open',
                             'skill': Skills.open_website_in_browser
                            ]
        """
        for skill in BASIC_SKILLS.values():
            if skill['enable']:
                for tag in skill['tags']:
                    if tag in self.latest_voice_transcript:
                        skill = {'voice_transcript': self.latest_voice_transcript,
                                 'tag': tag,
                                 'skill': skill['skill']}

                        logging.debug('Update skills queue with skill: {0}'.format(skill))
                        self.skills_to_execute.append(skill)

    def execute(self):
        """
        Execute one-by-one all the user skills and empty the queue with the waiting skills.
        """
        for skill in self.skills_to_execute:
            logging.debug('Execute the skill {0}'.format(skill))
            skill['skill'](**skill)

            # Remove the executed or not skill from the queue
            self.skills_to_execute.remove(skill)
