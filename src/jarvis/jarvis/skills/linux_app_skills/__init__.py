import subprocess
import logging
from jarvis.core.response import assistant_response


def open_new_bash(**kargs):
    """
    Opens new bash terminal
    """
    try:
        subprocess.Popen(['gnome-terminal'], stderr=subprocess.PIPE).communicate()
    except Exception as e:
        assistant_response("An error occurred, I can't open new bash terminal")
        logging.debug(e)


def open_note_app(**kargs):
    """
    Opens a note editor.
    """
    try:
        subprocess.Popen(['gedit'], stderr=subprocess.PIPE).communicate()
    except FileNotFoundError:
        assistant_response("You don't have installed the gedit")
        assistant_response("Install gedit with the following command: 'sudo apt-get install gedit'")


def open_new_browser_window(**kargs):
    """
    Opens new browser window.
    """
    try:
        subprocess.Popen(['firefox'], stderr=subprocess.PIPE).communicate()
    except Exception as e:
        assistant_response("An error occurred, I can't open firefox")
        logging.debug(e)
