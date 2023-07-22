from datetime import datetime
from secret import DB_NAME
from collections import defaultdict
import sqlite3


class Task:
    def __init__(self):
        self.tour = None
        self.num1 = None
        self.num2 = None
        self.ans  = None

    def load_from_row(self, task):
        self.tour = task[0]
        self.num1 = task[1]
        self.num2 = task[2]
        self.num1, self.num2 = int(self.num1), int(self.num2)
        if self.num1 > self.num2:
            self.num1, self.num2 = self.num2, self.num1
        self.ans = task[3]
    
    def load_base(self, tour, num1, num2, ans):
        self.tour = tour
        num1, num2 = int(num1), int(num2)
        if num1 > num2:
            num1, num2 = num2, num1
        self.num1 = num1
        self.num2 = num2
        self.ans = ans

    def __str__(self):
        self.num1, self.num2 = int(self.num1), int(self.num2)
        if self.num1 > self.num2:
            self.num1, self.num2 = self.num2, self.num1
        return f"{self.tour} {self.num1} {self.num2} {self.ans}"

    def is_correct_ans(self, ans):
        return self.check_ans(self.ans, ans)

    def check_ans(self, real_ans, given_ans):
        answers = real_ans.split('|')
        return given_ans in answers

class TaskCache:
    def __init__(self, param_for_db=DB_NAME):
        self.db_name = param_for_db
        self.conn = sqlite3.connect(self.db_name)
        self.tours = {
            "pro": defaultdict(Task),
            "novice": defaultdict(Task)
        }
        
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks(tour TEXT, name TEXT, ans TEXT);")
        self.conn.commit()

        cursor.execute("SELECT * FROM tasks;") # достаём из бд все задачи
        for task in cursor.fetchall():
            num1, num2 = int(task[1][0]), int(task[1][1])
            if num1 > num2:
                num1, num2 = num2, num1
            self.tours[task[0]][(num1, num2)].load_from_row([task[0], num1, num2, task[2]])
    
    def create_or_update_task(self, tour, num1, num2, ans):
        num1, num2 = int(num1), int(num2)
        if num1 > num2:
            num1, num2 = num2, num1
        if tour not in self.tours:
            return (False, "Такого турнира нет")
        if (num1, num2) in self.tours[tour]:
            return self.update_task(tour, num1, num2, ans)
        return self.new_task(tour, num1, num2, ans)

    def new_task(self, tour, num1, num2, ans):
        num1, num2 = int(num1), int(num2)
        if num1 > num2:
            num1, num2 = num2, num1
        task = Task()
        task.load_base(tour, num1, num2, ans)
        self.tours[tour][(num1, num2)] = task
        cursor = self.conn.cursor()
            
        entry = (tour, str(num1) + str(num2), ans)
        cursor.execute("INSERT INTO tasks VALUES(?, ?, ?);", entry) # кладём в бд
        self.conn.commit()

        return (True, "Задача добавлена")
    
    def update_task(self, tour, num1, num2, ans):
        num1, num2 = int(num1), int(num2)
        if num1 > num2:
            num1, num2 = num2, num1
        task = Task()
        task.load_base(tour, num1, num2, ans)
        self.tours[tour][(num1, num2)] = task
        cursor = self.conn.cursor()
            
        entry = (tour, ans, str(num1) + str(num2))
        cursor.execute("UPDATE tasks SET tour = ? ,  ans = ?  WHERE name = ? ;", entry)
        
        self.conn.commit()

        return (True, "Задача обновлена")
    
    def is_task(self, tour, num1, num2, ans):
        num1, num2 = int(num1), int(num2)
        if num1 > num2:
            num1, num2 = num2, num1
        if tour not in self.tours:
            return (False, "такого турнира нет")
        if (num1, num2) not in self.tours[tour]:
            return (False, "такой доминошки в этом турнире нет")
        return (True, "все ок")
   
    def check_task(self, tour, num1, num2, ans):
        num1, num2 = int(num1), int(num2)
        if num1 > num2:
            num1, num2 = num2, num1
        return self.tours[tour][(num1, num2)].is_correct_ans(ans=ans)

