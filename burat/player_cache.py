from secret import DB_NAME
from collections import defaultdict
import sqlite3

class Player:
    def __init__(self):
        self.user_id = None

        """
        1. фио
        2. название школы
        3. класс обучения (только число)
        4. населенный пункт
        5. регион
        6. телефон для связи
        7. *тренер/учитель/руководитель (при наличии) — фио, должность, место работы
        """
        self.fio = None
        self.school = None
        self.year = None
        self.city = None
        self.region = None
        self.phone = None
        self.trainer = None


    def load_from_row(self, row):
        self.user_id = row[0]
        self.tour = row[1]
        self.fio = row[2]
        self.allowed = row[3]
    

class PlayerCache:
    def __init__(self, param_for_db=DB_NAME):
        self.db_name = param_for_db
        self.conn = sqlite3.connect(self.db_name)
        self.players_storage = defaultdict(Player)
        
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS players(user_id TEXT PRIMARY KEY, tour TEXT, fio TEXT, allowed TEXT);")
        self.conn.commit()

        cursor.execute("SELECT * FROM players;")
        for player in cursor.fetchall():
            self.players_storage[player[0]].load_from_row(player)
    
    # def allow(self, user_id):
