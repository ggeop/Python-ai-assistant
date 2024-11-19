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

import logging
from jarvis.utils.skills_database import skillsDB

class SkillsRegistry:
    def __init__(self):
        self.skill_objects = []
        self.basic_skills = []
        self.control_skills = []

    @property
    def skill_objects(self):
        return self._skill_objects.copy()

    @skill_objects.setter
    def skill_objects(self, skill_objects):
        # logging.warn("setting skill_objects = %d" %len(skill_objects))
        self._skill_objects = skill_objects.copy()

    @property
    def basic_skills(self):
        # logging.warn("getting basic_skills %s" % type(self._basic_skills))
        return self._basic_skills.copy()

    @basic_skills.setter
    def basic_skills(self, basic_skills):
        # logging.warn("setting basic_skills = %d, %s" % (len(basic_skills), type(basic_skills)))
        self._basic_skills = basic_skills.copy()

    @property
    def control_skills(self):
        # logging.warn("getting control_skills %s" % type(self._control_skills))
        return self._control_skills.copy()

    @control_skills.setter
    def control_skills(self, control_skills):
        # logging.warn("setting control_skills = %d" % len(control_skills))
        self._control_skills = control_skills.copy()
    
    @property
    def learned_skills(self):
        return skillsDB.getLearnedSkills()

skills_registry = SkillsRegistry()
