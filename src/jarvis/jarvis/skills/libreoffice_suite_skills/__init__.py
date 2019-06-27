import subprocess

from jarvis.core.response import assistant_response


def _open_libreoffice_app(app):
    app_arg = '-' + app
    subprocess.Popen(['libreoffice', app_arg], stdout=subprocess.PIPE)
    assistant_response('I opened a new' + app + ' document..')


def open_libreoffice_calc(**kargs):
    """
    Opens libreoffice_suite_skills calc application
    """
    _open_libreoffice_app('calc')


def open_libreoffice_impress(**kargs):
    """
    Opens libreoffice_suite_skills impress application
    """
    _open_libreoffice_app('impress')


def open_libreoffice_writer(**kargs):
    """
    Opens libreoffice_suite_skills writer application
    """
    _open_libreoffice_app('writer')
