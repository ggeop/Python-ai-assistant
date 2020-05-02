# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import time
import requests
import logging
from playsound import playsound

from jarvis.utils import console
from jarvis.enumerations import MongoCollections
from jarvis.core.console import ConsoleManager


def play_activation_sound():
    """
    Plays a sound when the assistant enables.
    """
    utils_dir = os.path.dirname(__file__)
    activation_soundfile = os.path.join(utils_dir, '..', 'files', 'activation_sound.wav')
    playsound(activation_soundfile)


def internet_connectivity_check(url='http://www.google.com/', timeout=2):
    """
    Checks for internet connection availability based on google page.
    """
    console_manager = ConsoleManager()
    try:
        console_manager.console_output(info_log='Checking internet connection..')
        _ = requests.get(url, timeout=timeout)
        console_manager.console_output(info_log='Internet connection passed!')
        return True
    except requests.ConnectionError:
        console_manager.console_output(warn_log="No internet connection.")
        console_manager.console_output(warn_log="Skills with internet connection will not work")
        return False


def configure_MongoDB(db, settings):

    # ------------------------------------------------------------------------------------------------------------------
    # Load settings
    # ------------------------------------------------------------------------------------------------------------------

    # Only in first time or if 'general_settings' collection is deleted
    if db.is_collection_empty(collection=MongoCollections.GENERAL_SETTINGS.value):
        console.print_console_header()
        print('First time configuration..')
        console.print_console_header()
        time.sleep(1)

        default_assistant_name = settings.DEFAULT_GENERAL_SETTINGS['assistant_name']
        default_input_mode = settings.DEFAULT_GENERAL_SETTINGS['input_mode']
        default_response_in_speech = settings.DEFAULT_GENERAL_SETTINGS['response_in_speech']

        new_settings = {
            'assistant_name': default_assistant_name,
            'input_mode': default_input_mode,
            'response_in_speech': default_response_in_speech,
        }

        try:
            db.update_collection(collection=MongoCollections.GENERAL_SETTINGS.value, documents=[new_settings])
            console.print_console_header('Assistant Name')
            print('Assistant name- {0} configured successfully!'.format(default_assistant_name.lower()))
            print('Input mode - {0} configured successfully!'.format(default_input_mode))
            print('Speech response output- {0} configured successfully!'.format(default_response_in_speech))
            time.sleep(2)

        except Exception as e:
            logging.error('Failed to configure assistant settings with error message {0}'.format(e))

    # ------------------------------------------------------------------------------------------------------------------
    # Load skills
    # ------------------------------------------------------------------------------------------------------------------

    from jarvis.skills.registry import CONTROL_SKILLS, ENABLED_BASIC_SKILLS

    all_skills = {
        MongoCollections.CONTROL_SKILLS.value: CONTROL_SKILLS,
        MongoCollections.ENABLED_BASIC_SKILLS.value: ENABLED_BASIC_SKILLS,
    }
    for collection, documents in all_skills.items():
        db.update_collection(collection, documents)
