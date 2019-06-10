import subprocess

from jarvis.utils.response_utils import assistant_response


def open_libreoffice_calc(**kargs):
    """
    Opens libreoffice calc application
    """
    # TODO: Refactor all libreoffice methods in one
    subprocess.Popen(['libreoffice', '-calc'], stdout=subprocess.PIPE)
    assistant_response('I opened a new calc document..')
