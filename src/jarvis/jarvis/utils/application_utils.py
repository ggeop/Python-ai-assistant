import sys
import os
import requests
import traceback
import logging
from subprocess import call
from logging import config

from jarvis.settings import LOG_SETTINGS
from jarvis.utils.response_utils import assistant_response

jarvis_logo = "\n"\
"      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗\n"\
"      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝\n"\
"      ██║███████║██████╔╝██║   ██║██║███████╗\n"\
" ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║\n"\
" ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║\n"\
"  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝\n"


start_text = "\n"\
" ###############################################\n"\
" #    Jarvis Python Voice Assistant Platform   #\n"\
" ###############################################\n"


class OutputStyler:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    CYAN = '\033[36m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Create a Console & Rotating file logger
config.dictConfig(LOG_SETTINGS)


def log(func):
    """
    Logging wrapper
    :param func: function object
    """
    def wrapper(*args, **kwargs):
        try:
            logging.debug(func.__name__)
            func(*args, **kwargs)
        except Exception as e:
            logging.error(func.__name__)
            traceback.print_exc(file=sys.stdout)
    return wrapper


def clear():
    """
    Clear stdout
    """
    _ = call('clear' if os.name == 'posix' else 'cls')  # check and make call for specific operating system


def start_up():
    """
    Clear the console and print the assistant logo.
    """
    clear()
    print(OutputStyler.CYAN + jarvis_logo + OutputStyler.ENDC)
    print(OutputStyler.HEADER + start_text + OutputStyler.ENDC)


def internet_connectivity_check(url='http://www.google.com/', timeout=2):
    """
    Checks for internet connection availability based on google page.
    """
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        logging.info("No internet connection.")
        assistant_response("I inform you that I face internet connectivity problem")
    return False