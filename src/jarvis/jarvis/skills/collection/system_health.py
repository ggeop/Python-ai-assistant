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

import os
import psutil

from jarvis.skills.skill import AssistantSkill


class SystemHealthSkills(AssistantSkill):

    @classmethod
    def tell_memory_consumption(cls,**kwargs):
        """
        Responds the memory consumption of the assistant process.
        """
        memory = cls._get_memory_consumption()
        cls.response("I use {0:.2f} GB..".format(memory))

    @classmethod
    def _get_memory_consumption(cls):
        pid = os.getpid()
        py = psutil.Process(pid)
        memory_use = py.memory_info()[0] / 2. ** 30  # memory use in GB...I think
        return memory_use
