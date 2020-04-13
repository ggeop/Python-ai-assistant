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

import logging

from jarvis.skills.assistant_skill import AssistantSkill
from jarvis.utils.mongoDB import db

help_header = "------------------------------- Help -----------------------------------"


class AssistantInfoSkills(AssistantSkill):

    @classmethod
    def assistant_check(cls, **kwargs):
        """
        Responses that assistant can hear the user.
        """
        cls.response('Yes, I hear you!')

    @classmethod
    def tell_the_skills(cls, **kwargs):
        """
        Tells what he can do as assistant.

        NOTE: Use print instead cls.response() because we want only to print the response
        """
        try:
            response_base = 'I can do the following: \n\n'
            response = cls._create_skill_response(response_base)
            cls.response(response)
        except Exception as e:
            logging.error("Error with the execution of skill with message {0}".format(e))
            cls.response("Sorry I faced an issue")

    @classmethod
    def assistant_help(cls, **kwargs):
        """
        Assistant help prints valuable information about the application.

        NOTE: Use print instead cls.response() because we want only to print the response
        """
        print(help_header)
        response_base = ''
        try:
            response = cls._create_skill_response(response_base)
            print(response)
        except Exception as e:
            logging.error("Error with the execution of skill with message {0}".format(e))
            cls.response("Sorry I faced an issue")

    @classmethod
    def _create_skill_response(cls, response):

        # --------------------------------------------------------------------------------------------------------------
        # For existing skills (basic skills)
        # --------------------------------------------------------------------------------------------------------------
        basic_skills = db.get_documents(collection='enabled_basic_skills')
        response = response + '* Basic Enabled Skills:' + '\n'
        for skill_id, skill in enumerate(basic_skills, start=1):
            response = response + '{0}) '.format(skill_id) + skill.get('description') + '\n'

        # --------------------------------------------------------------------------------------------------------------
        # For learned skills (created from 'learn' skill)
        # --------------------------------------------------------------------------------------------------------------
        skills = db.get_documents(collection='learned_skills')
        response = response + '\n' + '* Learned Skills:' + '\n'
        for skill_id, skill in enumerate(skills, start=1):
            message = 'Learned skill - Q: ' + skill.get('tags') + ' | R: ' + skill.get('response')
            response = response + '{0}) '.format(skill_id) + message + '\n'

        return response
