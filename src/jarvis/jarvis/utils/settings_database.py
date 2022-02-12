import sqlite3
import json

class GeneralSettings:
    def __init__(self, input_mode='voice', assistant_name='jarvis', response_in_speech='true'):
        self.input_mode = input_mode
        self.assistant_name = assistant_name
        self.response_in_speech = response_in_speech
    def __str__(self):
        return "input_mode=%s, assistant_name=%s, response_in_speech=%s" % (
            self.input_mode, self.assistant_name, self.response_in_speech)

# class ControlSkills:
#     def __init__(self):
#         self.something = 0

# class EnabledBasicSkills:
#     def __init__(self):
#         self.something = 0

# class LearnedSkills:
#     def __init__(self):
#         self.something = 0


class SettingsDatabase:
    def __init__(self, database='settings.db'):
        self.database = database
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
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

#print("Create settings")
settingsDB = SettingsDatabase()
# print("Get settings")
# gen = settingsDB.getGeneralSettings()
# print("Gen = (%s)" % gen)
# gen.assistant_name = 'travis'
# settingsDB.updateGeneralSettings(gen)
# gen = settingsDB.getGeneralSettings()
# print("Gen = (%s)" % gen)
