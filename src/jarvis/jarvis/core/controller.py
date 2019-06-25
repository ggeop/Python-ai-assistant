import logging
import speech_recognition as sr

from datetime import datetime, timedelta

from jarvis.settings import GENERAL_SETTINGS
from jarvis.utils.response_utils import assistant_response, user_speech_playback
from jarvis.utils.application_utils import log, user_input, speech_interruption
from jarvis.skills.skills_registry import BASIC_SKILLS, CONTROL_SKILLS
from jarvis.setup import set_microphone
from jarvis.utils import application_utils

class Controller:
    def __init__(self):
        self.r = sr.Recognizer()
        if GENERAL_SETTINGS['user_voice_input']:
            self.microphone = set_microphone(self.r)
        self.skills_to_execute = []
        self.latest_voice_transcript = ''
        self.execute_state = {'ready_to_execute': False, 'enable_time': None}

    def wake_up_check(self):
        """
        Checks if the state of the skill manager (ready_to_execute)
        and if is not enabled search for enable word in user recorded speech.
        :return: boolean
        """
        if GENERAL_SETTINGS['user_voice_input']:
            if not self.execute_state['ready_to_execute']:
                return self._ready_to_start()
            else:
                return self._continue_listening()
        else:
            return True

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
            self._recognize_voice()
        else:
            self._recognize_text()

    def _recognize_text(self):
        logging.info("Waiting for user input..")
        self.latest_voice_transcript = input(user_input).lower()
        while self.latest_voice_transcript == '':
            assistant_response("Say something..")
            self.latest_voice_transcript = input(user_input).lower()
        if speech_interruption(self.latest_voice_transcript):
            self.latest_voice_transcript = ''
            logging.debug('Speech interruption')

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

    def _recognize_voice(self):
        audio = self._record()
        try:
            self.latest_voice_transcript = audio.lower()
            logging.debug('Recognized words: ' + self.latest_voice_transcript)
            if speech_interruption(self.latest_voice_transcript):
                self.latest_voice_transcript = ''
                logging.debug('Speech interruption')
        except sr.UnknownValueError:
            assistant_response('....')
        except sr.RequestError:
            assistant_response("Try later.. (Google API was unreachable..)")

    def _record(self):
        """
        Capture the user speech and transform it to audio stream (speech --> audio stream).
        """
        # Update microphone variables (Create these two global variables for user system printing)
        application_utils.dynamic_energy_ratio = self.r.dynamic_energy_ratio
        logging.debug('Dynamic energy ration value is: {0}'.format(application_utils.dynamic_energy_ratio))
        application_utils.energy_threshold = self.r.energy_threshold
        logging.debug('Energy threshold is: {0}'.format(application_utils.energy_threshold))

        with self.microphone as source:
            audio_text = self.r.listen(source)
            audio_text = input('here: ')
        return audio_text


class SkillsController(Controller):

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

                        logging.info('Add new skill: {0}'.format(skill['skill']))
                        self.skills_to_execute.append(skill)
                        logging.debug('skills_to_execute : {0}'.format(self.skills_to_execute))

    def execute(self):
        """
        Execute one-by-one all the user skills and empty the queue with the waiting skills.
        """
        for skill in self.skills_to_execute:
            try:
                logging.debug('Execute skill {0}'.format(skill))
                skill['skill'](**skill)
            except Exception as e:
                logging.debug("Error with the execution of skill {0} with message {1}".format(skill['skill'], e))

        # Clear the skills queue
        self.skills_to_execute = []
