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
import subprocess


def play_activation_sound():
    """
    Plays a sound when the assistant enables.
    """
    utils_dir = os.path.dirname(__file__)
    enable_sound = os.path.join(utils_dir, '..', 'files', 'enable_sound.wav')
    fnull = open(os.devnull, 'w')
    subprocess.Popen(['play', enable_sound], stdout=fnull, stderr=fnull).communicate()


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
    # ----------------------------------------------------------------------------------------------------------------------
    # Load settings in MongoDB
    # ----------------------------------------------------------------------------------------------------------------------
    configure = True
    if db.is_collection_empty(collection='general_settings'):
        print('-' * 48)
        print('Assistant is already configured.')
        print('-' * 48)
        configure = input('Do you want to configure it again (y/n): ').lower() == 'y'

    while configure:
        default_asssistant_name = settings.DEFAULT_GENERAL_SETTINGS['assistant_name']
        default_enabled_period = settings.DEFAULT_GENERAL_SETTINGS['enabled_period']
        default_response_in_text = settings.DEFAULT_GENERAL_SETTINGS['response_in_text']
        default_response_in_speech = settings.DEFAULT_GENERAL_SETTINGS['response_in_speech']

        print('Set assistant name (default is Jarvis')
        assistant_name = (input('Assistant name: ') or default_asssistant_name).lower()

        enable_period = input('Enable period (seconds): ') or default_enabled_period
        while not enable_period.isdigit():
            logging.info("Please give a number ONLY e.g 300, 100")
            enable_period = input('Enable period (seconds): ') or default_enabled_period

        response_in_text = (input('Response in txt (seconds) (y/n): ').lower() == 'y' or default_response_in_text)
        response_in_speech = (input('Response in speech (seconds) (y/n): ').lower() == 'y' or default_response_in_speech)

        new_settings = {
            'Assistant Name': assistant_name,
            'Enabled Period': enable_period,
            'Input Mode': 'text',  # TODO
            'Response in text': response_in_text,
            'Response in speech': response_in_speech,
        }

        print("\n The new settings are the following: \n")
        for setting_desc, value in new_settings.items():
            print('* {0}: {1}'.format(setting_desc, value))

        save_new_settings = input('Do you want to save new settings (y/n): ').lower() == 'y'

        if save_new_settings:
            db.update_collection(collection='general_settings', documents=new_settings)
            #TODO Add assistant name in greeding skill
            configure = False

    # ----------------------------------------------------------------------------------------------------------------------
    # Load skills in MongoDB
    # ----------------------------------------------------------------------------------------------------------------------
    from jarvis.skills.skills_registry import CONTROL_SKILLS, ENABLED_BASIC_SKILLS
    all_skills = {
        'control_skills': CONTROL_SKILLS,
        'enabled_basic_skills': ENABLED_BASIC_SKILLS,
    }
    for collection, documents in all_skills.items():
        db.update_collection(collection, documents)

    if not db.is_collection_empty(collection='learned_skills'):
        print("INFO: I found learned skills..")
        user_answer = input('Remove learned skills (y/n): ').lower()
        if user_answer == 'y':
            db.drop_collection(collection='learned_skills')
