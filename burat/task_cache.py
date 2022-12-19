from datetime import datetime
from secret import DB_NAME
from collections import defaultdict
import sqlite3

# DB_NAME = "C:\\KovalenkoDB\\marathon.txt"

class Task:
    def __init__(self):
        self.tour = None
        self.theme = None
        self.ans1 = None
        self.ans2 = None
        self.ans3 = None
        self.ans4 = None
        self.ans5 = None

    def load_from_row(self, task):
        self.tour = task[0]
        self.theme = task[1]
        self.ans1 = task[2]
        self.ans2 = task[3]
        self.ans3 = task[4]
        self.ans4 = task[5]
        self.ans5 = task[6]
    
    def load_base(self, tour, theme, ans1, ans2, ans3, ans4, ans5):
        self.tour = tour
        self.theme = theme
        self.ans1 = ans1
        self.ans2 = ans2
        self.ans3 = ans3
        self.ans4 = ans4
        self.ans5 = ans5

    def __str__(self):
        return "{} {} {} {} {} {} {}".format(self.tour, self.theme, self.ans1, self.ans2, self.ans3, self.ans4, self.ans5)

    def is_correct_ans(self, ans, taskid):
        if taskid == "1":
            return self.check_ans(self.ans1, ans)
        if taskid == "2":
            return self.check_ans(self.ans2, ans)
        if taskid == "3":
            return self.check_ans(self.ans3, ans)
        if taskid == "4":
            return self.check_ans(self.ans4, ans)
        if taskid == "5":
            return self.check_ans(self.ans5, ans)
        return False

    def check_ans(self, real_ans, given_ans):
        answers = real_ans.split('|')
        return given_ans in answers

class TaskCache:
    def __init__(self, param_for_db=DB_NAME):
        self.db_name = param_for_db
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.tours = {
            "pro": defaultdict(Task),
            "novice": defaultdict(Task)
        }
        
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks(tour TEXT, theme TEXT PRIMARY KEY, ans1 TEXT, ans2 TEXT, ans3 TEXT, ans4 TEXT, ans5 TEXT);")
        self.conn.commit()

        cursor.execute("SELECT * FROM tasks;")
        for task in cursor.fetchall():
            self.tours[task[0]][task[1]].load_from_row(task)
    
    def create_or_update_task(self, tour, theme, ans1, ans2, ans3, ans4, ans5):
        if tour not in self.tours:
            return (False, "Такого турнира нет")
        if theme in self.tours[tour]:
            return self.update_task(tour, theme, ans1, ans2, ans3, ans4, ans5)
        return self.new_task(tour, theme, ans1, ans2, ans3, ans4, ans5)

    def new_task(self, tour, theme, ans1, ans2, ans3, ans4, ans5):
        task = Task()
        task.load_base(tour, theme, ans1, ans2, ans3, ans4, ans5)
        self.tours[tour][theme] = task
        cursor = self.conn.cursor()
            
        entry = (tour, theme, ans1, ans2, ans3, ans4, ans5)
        cursor.execute("INSERT INTO tasks VALUES(?, ?, ?, ?, ?, ?, ?);", entry)
        self.conn.commit()

        return (True, "Задачи добавлены")
    
    def update_task(self, tour, theme, ans1, ans2, ans3, ans4, ans5):
        task = Task()
        task.load_base(tour, theme, ans1, ans2, ans3, ans4, ans5)
        self.tours[tour][theme] = task
        cursor = self.conn.cursor()
            
        entry = (tour, ans1, ans2, ans3, ans4, ans5, theme)
        cursor.execute("UPDATE tasks SET tour = ? ,  ans1 = ? , ans2 = ? , ans3 = ? , ans4 = ? , ans5  = ? WHERE theme = ? ;", entry)
        self.conn.commit()

        return (True, "Задачи обновлены")
    
    def is_task(self, tour, theme, taskid, ans):
        if tour not in self.tours:
            return (False, "такого турнира нет")
        if theme not in self.tours[tour]:
            return (False, "такой темы в этом турнире нет")
        if not (taskid >= "1" and taskid <= "5"):
            return (False, "некорректный номер задачи")
        return (True, "все ок")
   
    def check_task(self, tour, theme, taskid, ans):
        return self.tours[tour][theme].is_correct_ans(taskid=taskid, ans=ans)
        