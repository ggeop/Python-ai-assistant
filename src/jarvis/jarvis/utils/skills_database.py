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

import sqlite3
import json
from os.path import isdir, dirname

from jarvis.settings import DATABASE_SETTINGS

class SkillsDatabase:
    def __init__(self, database='skills.db'):
        self.database = database
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        if not isdir(dirname(self.database)):
            raise IOError("Database base dir %s does not exist" % dirname(self.database))

        conn = sqlite3.connect(self.database)
        conn.execute(
            """create table if not exists collections (
                data BLOB 
            ); """)
        conn.commit()
        conn.close()

    def hasLearnedSkills(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        rows = cursor.execute("select count(*) from collections").fetchall()
        conn.close()

        return rows[0][0] > 0

    def getLearnedSkills(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        rows = cursor.execute("select data from collections").fetchall()
        conn.close()

        response = []
        for row in rows:
            skill = json.loads(row[0].decode('utf-8'))
            response.append(skill)
        return response

    def addLearnedSkill(self, skill):
        blob = bytes(json.dumps(skill), 'utf-8')
        conn = sqlite3.connect(self.database)
        conn.execute(
            '''
            insert into collections(data) values (?)
            ''', (blob,))
        conn.commit()
        conn.close()
    
    def clearLearnedSkills(self):
        conn = sqlite3.connect(self.database)
        conn.execute(
            '''
            drop from collections(data)
            ''')
        conn.commit()
        conn.close()


skillsDB = SkillsDatabase(DATABASE_SETTINGS['base_dir'] + DATABASE_SETTINGS['skills_filename'])
