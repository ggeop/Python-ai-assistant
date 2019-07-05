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
import os
import psutil

from jarvis.utils.application_utils import clear, stdout_print, jarvis_logo, OutputStyler


class ConsoleManager:
    def __init__(self, log_settings):
        self.log_settings = log_settings
        # self.dynamic_energy_ratio = None
        # self.energy_threshold = None

    def console_output(self, text):
        clear()

        stdout_print(jarvis_logo)

        stdout_print("  NOTE: CTRL + C If you want to Quit.")

        print(OutputStyler.HEADER + '-------------- INFO --------------' + OutputStyler.ENDC)

        print(OutputStyler.HEADER + 'SYSTEM ---------------------------' + OutputStyler.ENDC)
        print(OutputStyler.BOLD +
              'RAM USAGE: {0:.2f} GB'.format(self._get_memory()) + OutputStyler.ENDC)

        # print(OutputStyler.HEADER + 'MIC ------------------------------' + OutputStyler.ENDC)
        # print(OutputStyler.BOLD +
        #       'ENERGY THRESHOLD LEVEL: ' + '|' * int(self.energy_threshold) + '\n'
        #       'DYNAMIC ENERGY LEVEL: ' + '|' * int(self.dynamic_energy_ratio) + OutputStyler.ENDC)
        # print(' ')

        print(OutputStyler.HEADER + '-------------- LOG --------------' + OutputStyler.ENDC)
        lines = subprocess.check_output(['tail', '-10', self.log_settings['handlers']['file']['filename']]).decode("utf-8")
        print(OutputStyler.BOLD + lines + OutputStyler.ENDC)

        print(OutputStyler.HEADER + '-------------- ASSISTANT --------------' + OutputStyler.ENDC)
        print(OutputStyler.BOLD + '> ' + text + '\r' + OutputStyler.ENDC)

    @staticmethod
    def _get_memory():
        pid = os.getpid()
        py = psutil.Process(pid)
        return py.memory_info()[0] / 2. ** 30  # memory use in GB...I think
