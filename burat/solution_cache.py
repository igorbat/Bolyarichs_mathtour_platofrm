from datetime import datetime
from burat.secret import DB_NAME
import sqlite3


class SolutionCache:
    def __init__(self, param_for_db=DB_NAME):
        self.db_name = param_for_db
        self.conn = sqlite3.connect(self.db_name)
        self.solution_storage = []
        
        cursor = self.conn.cursor()
        # cursor.execute("DROP TABLE solutions;")
        cursor.execute("CREATE TABLE IF NOT EXISTS solutions(user_id TEXT, theme TEXT, task_id TEXT, answer TEXT, timee INT);")
        self.conn.commit()

        cursor.execute("SELECT * FROM solutions;")
        for solution in cursor.fetchall():
            self.solution_storage.append([solution[0], solution[1], solution[2], solution[3], solution[4]])
    
    def new_solution(self, user_id, theme, task_id, answer, timee=int(datetime.timestamp(datetime.now()))):
        self.solution_storage.append([user_id, theme, task_id, answer, timee])
        cursor = self.conn.cursor()
            
        entry = (user_id, theme, task_id, answer, timee)
        cursor.execute("INSERT INTO solutions VALUES(?, ?, ?, ?, ?);", entry)
        self.conn.commit()
        return (True, "посылка принята")
    
    def solution_count(self, user_id):
        ans = 0
        for sol in self.solution_storage:
            if sol[0] == user_id:
                ans += 1
        return (True, ans)