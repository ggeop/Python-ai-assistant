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

from jarvis.skills.skill import AssistantSkill
from jarvis.utils.mongoDB import db
from jarvis.utils.console import headerize

basic_skills_format = """
-----------------------------------------------------------------------
- Basic Skills                                                        -
-----------------------------------------------------------------------
"""

basic_skills_body_format = """
---------------------------- Skill ({0}) ----------------------------
* Skill func: {1}
* Description: {2}
* Tags: {3}
"""

learned_skills_format = """
-----------------------------------------------------------------------
- Learned Skills                                                      -
-----------------------------------------------------------------------
"""

learned_skills_body_format = """
-------------------------- Learned Skill ({0}) ------------------------
* Skill func: {1}
* Question: {2}
* Response: {3}
"""


class AssistantInfoSkills(AssistantSkill):

    @classmethod
    def assistant_check(cls, **kwargs):
        """
        Responses that assistant can hear the user.
        """
        cls.response('Hey human!')

    @classmethod
    def tell_the_skills(cls, **kwargs):
        """
        Tells what he can do as assistant.
        """
        try:
            response_base = 'I can do the following: \n\n'
            response = cls._create_skill_response(response_base)
            cls.response(response)
        except Exception as e:
            cls.console(error_log="Error with the execution of skill with message {0}".format(e))
            cls.response("Sorry I faced an issue")

    @classmethod
    def assistant_help(cls, **kwargs):
        """
        Assistant help prints valuable information about the application.

        """
        cls.console(headerize('Help'))
        response_base = ''
        try:
            response = cls._create_skill_response(response_base)
            cls.console(response)
        except Exception as e:
            cls.console(error_log="Error with the execution of skill with message {0}".format(e))
            cls.response("Sorry I faced an issue")

    @classmethod
    def _create_skill_response(cls, response):

        # --------------------------------------------------------------------------------------------------------------
        # For existing skills (basic skills)
        # --------------------------------------------------------------------------------------------------------------
        basic_skills = db.get_documents(collection='enabled_basic_skills')
        response = response + basic_skills_format
        for skill_id, skill in enumerate(basic_skills, start=1):
            response = response + basic_skills_body_format.format(skill_id,
                                                                  skill.get('name'),
                                                                  skill.get('description'),
                                                                  skill.get('tags')
                                                                  )

        # --------------------------------------------------------------------------------------------------------------
        # For learned skills (created from 'learn' skill)
        # --------------------------------------------------------------------------------------------------------------
        skills = db.get_documents(collection='learned_skills')
        response = response + learned_skills_format
        for skill_id, skill in enumerate(skills, start=1):
            response = response + learned_skills_body_format.format(skill_id,
                                                                    skill.get('name'),
                                                                    skill.get('tags'),
                                                                    skill.get('response')
                                                                    )

        return response
