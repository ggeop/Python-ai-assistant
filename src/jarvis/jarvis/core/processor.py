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

from jarvis.core.controller import SkillsController
from jarvis.utils.application_utils import start_up
from jarvis.skills.wolframalpha_skill import call_wolframalpha


class Processor:
    def __init__(self):
        self.controller = SkillsController()

    def run(self):
        start_up()
        while True:
            self._process()

    def _process(self):
        # Check if the assistant is waked up
        if self.controller.wake_up_check():

            self.controller.get_transcript()
            self.controller.get_skills()

            if self.controller.to_execute:
                self.controller.execute()
            else:
                self.controller.shutdown_check()

                # If there is not an action the assistant make a request in WolframAlpha API
                call_wolframalpha(self.controller.latest_voice_transcript)

        self.controller.shutdown_check()
