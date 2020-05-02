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
import jarvis


def get_master_volume():
    stdout, stderr = subprocess.Popen('/usr/bin/amixer sget Master', shell=True,
                                      stdout=subprocess.PIPE).communicate()
    list_len = len(str(stdout).split('\n'))
    amixer_stdout = str(stdout).split('\n')[list_len - 1]

    find_start = amixer_stdout.find('[') + 1
    find_end = amixer_stdout.find('%]', find_start)

    return float(amixer_stdout[find_start:find_end])


def set_master_volume(volume):
    val = float(int(volume))

    proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
    proc.wait()


class UtilSkills(AssistantSkill):

    @classmethod
    def speech_interruption(cls, **kwargs):
        """
        Stop assistant speech.
        """
        jarvis.output_engine.stop_speaking = True

    @classmethod
    def clear_console(cls, **kwargs):
        cls.console("Sure")

    @classmethod
    def increase_master_volume(cls, **kwargs):
        # Limits: Playback 0 - 31
        step = 2
        volume = get_master_volume()
        if volume > 31:
            cls.response("The speakers volume is already max")

        increased_volume = volume + step
        if increased_volume > 31:
            set_master_volume(31)
        else:
            set_master_volume(increased_volume)
            cls.response("I increased the speakers volume")

    @classmethod
    def reduce_master_volume(cls, **kwargs):
        # Limits: Playback 0 - 31
        step = 2
        volume = get_master_volume()
        if volume < 0:
            cls.response("The speakers volume is already muted")

        reduced_volume = volume - step
        if reduced_volume < 0:
            set_master_volume(0)
        else:
            set_master_volume(reduced_volume)
            cls.response("I reduced the speakers volume")

    @classmethod
    def mute_master_volume(cls, **kwargs):
        # Limits: Playback 0 - 31
        volume = get_master_volume()
        if volume == 0:
            cls.response("The speakers volume is already muted")
        else:
            set_master_volume(0)
            cls.response("I mute the master speakers")

    @classmethod
    def max_master_volume(cls, **kwargs):
        # Limits: Playback 0 - 31
        volume = get_master_volume()
        if volume == 31:
            cls.response("The speakers volume is already max")
        else:
            set_master_volume(31)
            cls.response("I set max the master speakers")
