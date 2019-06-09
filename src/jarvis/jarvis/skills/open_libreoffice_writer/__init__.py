import subprocess

from jarvis.utils.response_utils import assistant_response


def open_libreoffice_writer(**kargs):
    """
    Opens libreoffice writer application
    """
    subprocess.Popen(['libreoffice', '-writer'], stdout=subprocess.PIPE)
    assistant_response('I opened a new writer document..')