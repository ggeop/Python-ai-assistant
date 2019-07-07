# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import time
import requests
import traceback
import logging
import subprocess

from subprocess import call
from logging import config

import jarvis.core.memory
from jarvis.settings import ROOT_LOG_CONF
from jarvis._version import __version__

jarvis_logo = "\n" \
              "      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗\n" \
              "      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝\n" \
              "      ██║███████║██████╔╝██║   ██║██║███████╗\n" \
              " ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║\n" \
              " ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║\n" \
              "  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝"

start_text = "" \
             " -----------------------------------------------\n" \
             " -  Voice Assistant Platform  " + "v" + __version__ + "-\n" \
             " -----------------------------------------------\n"


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


user_input = OutputStyler.CYAN + '>> ' + OutputStyler.ENDC

# Create a Console & Rotating file logger
config.dictConfig(ROOT_LOG_CONF)


def log(func):
    """
    Logging wrapper
    :param func: function object
    """
    def wrapper(*args, **kwargs):
        try:
            logging.debug(func.__name__)
            func(*args, **kwargs)
        except Exception:
            logging.error(func.__name__)
            traceback.print_exc(file=sys.stdout)
    return wrapper


def clear():
    """
    Clear stdout
    """
    _ = call('clear' if os.name == 'posix' else 'cls')  # check and make call for specific operating system


def internet_connectivity_check(url='http://www.google.com/', timeout=2):
    """
    Checks for internet connection availability based on google page.
    """
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        logging.info("No internet connection.")
        return False


def startup_ckecks():
    """
    Initial checks
    """

    print("=" * 48)
    print("Startup ckeck")
    print("=" * 48)

    print("INFO: Internet connection check..")
    if not internet_connectivity_check():
        stdout_print("WARNING: No internet connection, skills with internet connection will not work")
        time.sleep(3)


def start_up():
    """
    Do initial checks, clear the console and print the assistant logo.
    """
    startup_ckecks()
    clear()
    print(OutputStyler.CYAN + jarvis_logo + OutputStyler.ENDC)
    print(OutputStyler.HEADER + start_text + OutputStyler.ENDC)
    print(OutputStyler.HEADER + 'Waiting..' + OutputStyler.ENDC)

    # Clear log file in each assistant fresh start
    with open(ROOT_LOG_CONF['handlers']['file']['filename'], 'r+') as f:
        f.truncate(0)

    logging.info('APPLICATION STARTED..')


def play_activation_sound():
    """
    Plays a sound when the assistant enables.
    """
    utils_dir = os.path.dirname(__file__)
    enable_sound = os.path.join(utils_dir, '..', 'files', 'enable_sound.wav')
    fnull = open(os.devnull, 'w')
    subprocess.Popen(['play', enable_sound], stdout=fnull, stderr=fnull).communicate()


def user_speech_playback(text):
    """
    Prints the user commands in text.
    :param text: string
    """
    print(user_input)


def stdout_print(text):
    """
    Application stdout with format.
    :param text: string
    """
    print(OutputStyler.CYAN + text + OutputStyler.ENDC)