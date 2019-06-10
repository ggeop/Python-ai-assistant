import subprocess

from jarvis.utils.response_utils import assistant_response


def open_libreoffice_calc(**kargs):
    """
    Opens libreoffice_suite_skills calc application
    """
    # TODO: Refactor all libreoffice_suite_skills methods in one
    subprocess.Popen(['libreoffice_suite_skills', '-calc'], stdout=subprocess.PIPE)
    assistant_response('I opened a new calc document..')


def open_libreoffice_impress(**kargs):
    """
    Opens libreoffice_suite_skills impress application
    """
    subprocess.Popen(['libreoffice_suite_skills', '-impress'], stdout=subprocess.PIPE)
    assistant_response('I opened a new impress document..')



def open_libreoffice_writer(**kargs):
    """
    Opens libreoffice_suite_skills writer application
    """
    subprocess.Popen(['libreoffice_suite_skills', '-writer'], stdout=subprocess.PIPE)
    assistant_response('I opened a new writer document..')