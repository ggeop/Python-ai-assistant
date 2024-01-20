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

class GeneralSettings:
    def __init__(self, input_mode='voice', assistant_name='jarvis', response_in_speech='true'):
        self.input_mode = input_mode
        self.assistant_name = assistant_name
        self.response_in_speech = response_in_speech
    def __str__(self):
        return "input_mode=%s, assistant_name=%s, response_in_speech=%s" % (
            self.input_mode, self.assistant_name, self.response_in_speech)

class SettingsDatabase:
    def __init__(self, database='settings.db'):
        self.database = database
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        if not isdir(dirname(self.database)):
            raise IOError("Database base dir %s does not exist" % dirname(self.database))

        conn = sqlite3.connect(self.database)
        conn.execute(
            """create table if not exists collections (
                name VARCHAR(255) PRIMARY KEY,
                data BLOB 
            ); """)
        conn.commit()
        conn.close()

    def hasGeneralSettings(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        rows = cursor.execute("select data from collections where name = 'general_settings'").fetchall()
        conn.close()

        return len(rows) > 0

    def getGeneralSettings(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        rows = cursor.execute("select data from collections where name = 'general_settings'").fetchall()
        conn.close()

        if len(rows) < 1:
            return GeneralSettings()

        settings = json.loads(rows[0][0].decode('utf-8'))
        return GeneralSettings(
            input_mode = settings['input_mode'],
            response_in_speech = settings['response_in_speech'],
            assistant_name = settings['assistant_name']
        )
    
    def updateGeneralSettings(self, settings):
        blob = bytes(json.dumps(settings.__dict__), 'utf-8')
        conn = sqlite3.connect(self.database)
        conn.execute(
            '''
            insert into collections(name, data) values ('general_settings', ?)
            on conflict(name) do update set data=excluded.data;
            ''', (blob,))
        conn.commit()
        conn.close()

settingsDB = SettingsDatabase(DATABASE_SETTINGS['base_dir'] + DATABASE_SETTINGS['settings_filename'])
