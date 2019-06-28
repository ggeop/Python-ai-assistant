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
from jarvis.core.response import assistant_response


def assistant_check(**kargs):
    """
    Responses that assistant can hear the user.
    """
    assistant_response('Yes, I hear you!')


def _create_skill_response(response):
    for skill_id, skill in enumerate(skills_registry.BASIC_SKILLS.values()):
        response = response + '{0}) '.format(skill_id + 1) + skill['description'] + '\n'
    return response


def tell_the_skills(**kwargs):
    """
    Tells what he can do as assistant.
    """
    response_base = 'I can do the following: \n\n'
    response = _create_skill_response(response_base)
    response.assistant_response(response)


def assistant_help(**kwargs):
    """
    Assistant help prints valuable information about the application.
    """

    print("---- Help ----")
    print("Assistant skills: ")
    response_base = ''
    response = _create_skill_response(response_base)
    print(response)
