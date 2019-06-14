import subprocess

from jarvis.utils.response_utils import assistant_response


def open_note_app(**kargs):
    """
    Opens a note editor.
    """
    try:
        subprocess.Popen(['gedit'], stderr=subprocess.PIPE).communicate()
    except FileNotFoundError:
        assistant_response("You don't have installed the gedit")
        assistant_response("Install gedit with the following command: 'sudo apt-get install gedit'")

