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

from jarvis.skills.skill import AssistantSkill


class LibreofficeSkills(AssistantSkill):

    @classmethod
    def open_libreoffice_calc(cls, **kwargs):
        """
        Opens libreoffice_suite_skills calc application.
        """
        cls._open_libreoffice_app('calc')

    @classmethod
    def open_libreoffice_impress(cls, **kwargs):
        """
        Opens libreoffice_suite_skills impress application.
        """
        cls._open_libreoffice_app('impress')

    @classmethod
    def open_libreoffice_writer(cls, **kwargs):
        """
        Opens libreoffice_suite_skills writer application.
        """
        cls._open_libreoffice_app('writer')

    @classmethod
    def _open_libreoffice_app(cls, app):
        app_arg = '-' + app
        subprocess.Popen(['libreoffice', app_arg], stdout=subprocess.PIPE, shell=False)
        cls.console('I opened a new' + app + ' document..')
