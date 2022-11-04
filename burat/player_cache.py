from burat.secret import DB_NAME
from collections import defaultdict
import sqlite3

# DB_NAME = "C:\\KovalenkoDB\\marathon.txt"

class Player:
    def __init__(self):
        self.user_id = None
        self.fixed = False
        self.joined = "No registration"
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
        self.joined = "Принят"
        self.fixed = True


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
    
        self.fio = None
        self.school = None
        self.year = None
        self.city = None
        self.region = None
        self.phone = None
        self.trainer = None

    def set_fio(self, id, fio):
        self.players_storage[id].fio = fio
        return True, "ФИО Сохранено"
    
    def set_school(self, id, school):
        self.players_storage[id].school = school
        return True, "Школа Сохранена"
    
    def set_year(self, id, year):
        self.players_storage[id].year = year
        return True, "Класс Сохранен"

    def set_city(self, id, city):
        self.players_storage[id].city = city
        return True, "Населенный пункт Сохранен"
    
    def set_region(self, id, region):
        self.players_storage[id].region = region
        return True, "Регион Сохранен"
    
    def set_phone(self, id, phone):
        self.players_storage[id].phone = phone
        return True, "Телефон Сохранен"
    
    def set_trainer(self, id, trainer):
        if self.players_storage[id].fixed:
            return False, "Анкета на рассмотрении"
        self.players_storage[id].trainer = trainer
        return True, "Тренер Сохранен"
    
    def set_fixed(self, id):
        self.players_storage[id].fixed = True
        return True, "Анкета отправлена"
    
    def set_unfixed(self, id):
        self.players_storage[id].fixed = False
        return True, "Анкета вернулась учащемуся"
    # def allow(self, user_id):
