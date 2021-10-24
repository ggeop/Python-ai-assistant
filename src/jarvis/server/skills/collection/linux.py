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

import subprocess
import logging
import time

from jarvis.skills.skill import AssistantSkill


class LinuxAppSkills(AssistantSkill):

    @classmethod
    def open_new_bash(cls, **kwargs):
        """
        Opens new bash terminal.
        """
        try:
            subprocess.Popen(['gnome-terminal'], stderr=subprocess.PIPE, shell=False).communicate()
        except Exception as e:
            cls.response("An error occurred, I can't open new bash terminal")
            logging.debug(e)

    @classmethod
    def open_note_app(cls, **kwargs):
        """
        Opens a note editor (gedit).
        """
        try:
            subprocess.Popen(['gedit'], stderr=subprocess.PIPE, shell=False).communicate()
        except FileNotFoundError:
            cls.response("You don't have installed the gedit")
            time.sleep(2)
            cls.response("Install gedit with the following command: 'sudo apt-get install gedit'")

    @classmethod
    def open_new_browser_window(cls, **kwargs):
        """
        Opens new browser window.
        """
        try:
            subprocess.Popen(['firefox'], stderr=subprocess.PIPE, shell=False).communicate()
        except Exception as e:
            cls.response("An error occurred, I can't open firefox")
            logging.debug(e)