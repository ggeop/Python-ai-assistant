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

from jarvis.skills import skills_registry

from jarvis.skills.skill_manager import AssistantSkill


class AssistantInfoSkills(AssistantSkill):

    @classmethod
    def assistant_check(cls, **kwargs):
        """
        Responses that assistant can hear the user.
        """
        print('Yes, I hear you!')

    @classmethod
    def _create_skill_response(cls, response):
        for skill_id, skill in enumerate(skills_registry.BASIC_SKILLS.values()):
            response = response + '{0}) '.format(skill_id + 1) + skill['description'] + '\n'
        return response

    @classmethod
    def tell_the_skills(cls, **kwargs):
        """
        Tells what he can do as assistant.
        
        response_base = 'I can do the following: \n\n'
        response = cls._create_skill_response(response_base)
        response.assistant_response(response)#That doesn't work str has no attribut assistant_response
        #But that works:
         """
        try:
            response_base = 'I can do the following: \n\n'
            response = cls._create_skill_response(response_base)
            # response.assistant_response(response) For testing but that just won't work so cls.response() is the easiest fix xD
            cls.response(response)
        except Exception as e:
            print("Error with the execution of skill with message {0}".format(e)) #Just in case something  doesn't work, we get an error code

    @classmethod
    def assistant_help(cls, **kwargs):
        """
        Assistant help prints valuable information about the application.
        """
        print("---- Help ----")
        print("Assistant skills: ")
        response_base = ''
        response = cls._create_skill_response(response_base)
        print(response)
