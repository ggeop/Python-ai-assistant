import sqlite3
from time import time

class History:
    def __init__(self, user_transcript = '--', response = '--', executed_skill = '--', timestamp=0):
        self.user_transcript = user_transcript
        self.response = response
        self.executed_skill = executed_skill
        self.timestamp = timestamp if timestamp != 0 else int(time() * 1000)

    def __str__(self):
        return "user_transcript=%s, response=%s, executed_skill=%s, timestamp=%s" % (
            self.user_transcript, self.response, self.executed_skill, self.timestamp)

    def __repr__(self):
        return self.__str__()

class HistoryDatabase:
    def __init__(self, database='history.db'):
        self.database = database
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        conn = sqlite3.connect(self.database)
        conn.execute(
            """create table if not exists history (
                timestamp INTEGER PRIMARY KEY,
                user_transcript TEXT,
                response TEXT,
                executed_skill TEXT
            ); """)
        conn.commit()
        conn.close()

    def getHistory(self, limit = 3):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        rows = cursor.execute("select * from history order by timestamp DESC limit ?", (limit,)).fetchall()
        conn.close()

        response = []
        for row in rows:
            response.append(History(
                timestamp=row[0],
                user_transcript=row[1],
                response = row[2],
                executed_skill = row[3]))

        print("Returned %d history items" % len(response))
        return response

    def addHistory(self, history):
        conn = sqlite3.connect(self.database)
        conn.execute(
            '''
            insert into history
            (timestamp, user_transcript, response, executed_skill) values
            (?, ?, ?, ?)
            ''', (history.timestamp, history.user_transcript, history.response, history.executed_skill,))
        conn.commit()
        conn.close()

historyDB = HistoryDatabase()
# his = historyDB.getHistory()
# print("history = %s" % his)
# historyDB.addHistory(History(user_transcript='test1', response='resp1', executed_skill='skill1'))
# historyDB.addHistory(History(user_transcript='test2', response='resp2', executed_skill='skill2'))
# historyDB.addHistory(History(user_transcript='test3', response='resp3', executed_skill='skill3'))
# his = historyDB.getHistory(limit=3)
# for h in his:
#     print (h)
