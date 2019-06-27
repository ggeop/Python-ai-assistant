from jarvis.skills import skills_registry
from jarvis.core import response
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
