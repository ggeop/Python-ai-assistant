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
from pymongo import MongoClient
from jarvis.skills.skills_registry import BASIC_SKILLS, CONTROL_SKILLS


def _convert_skill_object_to_str(skill):
    for sk in skill:
        sk.update((k, v.__name__) for k, v in sk.items() if k == 'skill')


ENABLED_BASIC_SKILLS = [skill for skill in BASIC_SKILLS if skill['enable']]
SKILLS = CONTROL_SKILLS + ENABLED_BASIC_SKILLS

_convert_skill_object_to_str(BASIC_SKILLS)
_convert_skill_object_to_str(CONTROL_SKILLS)


class MongoDB:

    def __init__(self, host='localhost', port=27017, database='skills'):
        self.client = MongoClient(host, port)
        self.database = self.client[database]
        self._initialize_db()

    def _initialize_db(self, database='skills'):
        self.client.drop_database(database)

        self.insert_to_table('basic_skills', BASIC_SKILLS)
        self.insert_to_table('control_skills', CONTROL_SKILLS)
        self.insert_to_table('enabled_basic_skills', ENABLED_BASIC_SKILLS)
        self.insert_to_table('skills', SKILLS)

    def get_from_table(self, table_name, key=None):
        table_obj = self.database[table_name]
        return table_obj.find(key)

    def insert_to_table(self, table_name, values):
        table_obj = self.database[table_name]
        table_obj.insert_many(values)


def start_mongoDB_server():
    stopMongoServerCommand = "sudo service mongod start"
    process = subprocess.Popen(stopMongoServerCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    logging.info(output)


def stop_mongoDB_server():
    stopMongoServerCommand = "sudo service mongod stop"
    process = subprocess.Popen(stopMongoServerCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    logging.info(output)
