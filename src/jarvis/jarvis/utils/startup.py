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
import requests
import logging

from jarvis.utils import user_input, console
from jarvis.enumerations import InputMode, MongoCollections
from playsound import playsound


def play_activation_sound():
    """
    Plays a sound when the assistant enables.
    """
    utils_dir = os.path.dirname(__file__)
    activation_soundfile = os.path.join(utils_dir, '..', 'files', 'enable_sound.wav')
    playsound(activation_soundfile)


def internet_connectivity_check(url='http://www.google.com/', timeout=2):
    """
    Checks for internet connection availability based on google page.
    """
    try:
        logging.debug('Internet connection check..')
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        logging.warning("No internet connection.")
        return False


def configure_MongoDB(db, settings):
    # ------------------------------------------------------------------------------------------------------------------
    # Load skills
    # ------------------------------------------------------------------------------------------------------------------

    from jarvis.skills.skills_registry import CONTROL_SKILLS, ENABLED_BASIC_SKILLS

    all_skills = {
        MongoCollections.CONTROL_SKILLS.value: CONTROL_SKILLS,
        MongoCollections.ENABLED_BASIC_SKILLS.value: ENABLED_BASIC_SKILLS,
    }
    for collection, documents in all_skills.items():
        db.update_collection(collection, documents)

    # ------------------------------------------------------------------------------------------------------------------
    # Load settings
    # ------------------------------------------------------------------------------------------------------------------

    # Only in first time or if 'general_settings' collection is deleted
    if db.is_collection_empty(collection=MongoCollections.GENERAL_SETTINGS.value):
        console.print_console_header()
        print('First time configuration')
        console.print_console_header()
        configure = True

        while configure:
            default_enabled_period = settings.DEFAULT_GENERAL_SETTINGS['enabled_period']
            default_input_mode = settings.DEFAULT_GENERAL_SETTINGS['input_mode']
            default_response_in_speech = settings.DEFAULT_GENERAL_SETTINGS['response_in_speech']

            console.print_console_header('Assistant Name')
            print('NOTE: Set assistant name (default: Jarvis), you can activate assistant with this name')
            assistant_name = input('New assistant name: ').lower()

            console.print_console_header('Enable Period')
            print(
                'NOTE: Enable period is the duration without need activation word to execute a command (default: {0} '
                'seconds) '
                .format(default_enabled_period))
            enable_period = user_input.validate_digits_input('New enable period (seconds): ')

            console.print_console_header('Input Mode')
            print('NOTE: Set the type of the user input text or voice (default: {0})'.format(default_input_mode))
            print('* text: Write in console')
            print('* voice: Talk in microphone')
            input_mode_values = [mode.value for mode in InputMode]
            input_mode = user_input.validate_input_with_choices(message='Set input mode: ',
                                                                available_choices=input_mode_values)

            console.print_console_header('Response in Speech')
            print('NOTE: Choose also speech response output (default: {0})'.format(default_response_in_speech))
            response_in_speech = user_input.check_input_to_continue('Response in speech')

            new_settings = {
                'assistant_name': assistant_name,
                'enabled_period': enable_period,
                'input_mode': input_mode,
                'response_in_speech': response_in_speech,
            }

            print("\n The new settings are the following: \n")
            for setting_desc, value in new_settings.items():
                print('* {0}: {1}'.format(setting_desc, value))

            save_new_settings = input('Do you want to save new settings (y/n): ').lower() in ['y', 'yes']

            if save_new_settings:
                db.update_collection(collection=MongoCollections.GENERAL_SETTINGS.value, documents=[new_settings])
                configure = False

    # --------------------------------------------------------------------------------------------------------------
    # Update skills from settings
    # --------------------------------------------------------------------------------------------------------------

    # Add assistant name in  skill 'enable_assistant' + 'assistant_check' tags
    assistant_name = db.get_documents(collection=MongoCollections.GENERAL_SETTINGS.value)[0]['assistant_name']

    # Update enable_assistant skill
    existing_enable_assistant_tags = db.get_documents(collection=MongoCollections.CONTROL_SKILLS.value,
                                                      key={'name': 'enable_assistant'})[0]['tags']
    new_enable_assistant_tags = {'tags': existing_enable_assistant_tags + ' ' + assistant_name}
    db.update_document(collection=MongoCollections.CONTROL_SKILLS.value,
                       query={'name': 'enable_assistant'},
                       new_value=new_enable_assistant_tags
                       )

    # Update assistant_check
    existing_assistant_check_tags = db.get_documents(collection=MongoCollections.ENABLED_BASIC_SKILLS.value,
                                                     key={'name': 'assistant_check'})[0]['tags']
    new_assistant_check_tags = {'tags': existing_assistant_check_tags + ' ' + assistant_name}
    db.update_document(collection=MongoCollections.ENABLED_BASIC_SKILLS.value,
                       query={'name': 'assistant_check'},
                       new_value=new_assistant_check_tags
                       )
