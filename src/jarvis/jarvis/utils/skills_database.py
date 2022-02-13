from signal import pause
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
