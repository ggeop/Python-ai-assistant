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
