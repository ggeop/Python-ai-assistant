import subprocess

from jarvis.utils.response_utils import assistant_response


def open_libreoffice_impress(**kargs):
    """
    Opens libreoffice impress application
    """
    subprocess.Popen(['libreoffice', '-impress'], stdout=subprocess.PIPE)
    assistant_response('I opened a new impress document..')