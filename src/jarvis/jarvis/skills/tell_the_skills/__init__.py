import time
from jarvis.skills import skills_registry
from jarvis.utils import response_utils


def tell_the_skills(**kwargs):
    response = 'I can do the following: \n\n'

    for skill_id, skill in enumerate(skills_registry.BASIC_SKILLS.values()):
        response = response + '{0}) '.format(skill_id + 1) + skill['description'] + '\n'

    response_utils.assistant_response("xmm")
    response_utils.assistant_response("Good question..")
    time.sleep(1)
    response_utils.assistant_response("I can do a lot of things..")
    time.sleep(1)
    response_utils.assistant_response(response)
