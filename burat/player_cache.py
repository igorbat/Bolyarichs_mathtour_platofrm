from secret import DB_NAME
from collections import defaultdict
import sqlite3

# DB_NAME = "C:\\KovalenkoDB\\marathon.txt"

class Player:
    def __init__(self):
        self.user_id = None
        self.fixed = False
        self.allowed = False
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
        self.tour = None


    def load_from_row(self, row):
        self.user_id = row[0]
        self.tour = row[1]
        self.fio = row[2]
        self.regg = row[3]
        self.fixed = True
        self.allowed = True

class PlayerCache:
    def __init__(self, param_for_db=DB_NAME):
        self.db_name = param_for_db
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.players_storage = defaultdict(Player)
        
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS players(user_id TEXT PRIMARY KEY, tour TEXT, fio TEXT, reggi TEXT);")
        self.conn.commit()

        cursor.execute("SELECT * FROM players;")
        for player in cursor.fetchall():
            self.players_storage[player[0]].load_from_row(player)

    def set_fio(self, id, fio):
        if self.players_storage[id].fixed:
            return False, "Анкета на рассмотрении"
        self.players_storage[id].fio = fio
        return True, "ФИО Сохранено"
    
    def set_school(self, id, school):
        if self.players_storage[id].fixed:
            return False, "Анкета на рассмотрении"
        self.players_storage[id].school = school
        return True, "Школа Сохранена"
    
    def set_year(self, id, year):
        if self.players_storage[id].fixed:
            return False, "Анкета на рассмотрении"
        self.players_storage[id].year = year
        return True, "Класс Сохранен"

    def set_city(self, id, city):
        if self.players_storage[id].fixed:
            return False, "Анкета на рассмотрении"
        self.players_storage[id].city = city
        return True, "Населенный пункт Сохранен"
    
    def set_region(self, id, region):
        if self.players_storage[id].fixed:
            return False, "Анкета на рассмотрении"
        self.players_storage[id].region = region
        return True, "Регион Сохранен"
    
    def set_phone(self, id, phone):
        if self.players_storage[id].fixed:
            return False, "Анкета на рассмотрении"
        self.players_storage[id].phone = phone
        return True, "Телефон Сохранен"
    
    def set_trainer(self, id, trainer):
        if self.players_storage[id].fixed:
            return False, "Анкета на рассмотрении"
        self.players_storage[id].trainer = trainer
        return True, "Тренер Сохранен"
    
    def set_tour(self, id, tour):
        if self.players_storage[id].fixed:
            return False, "Анкета на рассмотрении"
        if tour != "pro" and tour != "novice": # TODO: Remove HardCode
            return False, "Такого турнира нет"
        self.players_storage[id].tour = tour
        return True, "Выбранный турнир Сохранен"
    
    def set_fixed(self, id):
        if self.players_storage[id].fixed:
            return False, "Анкета на рассмотрении", ""
        if self.players_storage[id].fio is None:
            return False, "Не сохранено ФИО", ""
        # if self.players_storage[id].school is None:
        #     return False, "Не сохранена школа", ""
        # if self.players_storage[id].year is None:
        #     return False, "Не сохранено класс обучения, например, 7", ""
        # if self.players_storage[id].city is None:
        #     return False, "Не сохранено населенный пункт", ""
        # if self.players_storage[id].region is None:
        #     return False, "Не сохранено регион", ""
        # if self.players_storage[id].phone is None:
        #     return False, "Не сохранено номер телефона", ""
        # if self.players_storage[id].trainer is None:
        #     return False, "Не сохранено ФИО Тренера(Учителя), должность и место работы ", ""
        # if self.players_storage[id].tour is None:
        #     return False, "Не сохранен выбранный турнир: pro или novice", ""    
        self.players_storage[id].fixed = True
        return True, "Анкета отправлена", "НОВЫЙ УЧАСТНИК: id = {} \nФИО:{}\nШКОЛА:{}\nКЛАСС:{}\nГОРОД:{}\nРЕГИОН:{}\nТЕЛЕФОН:{}\nТРЕНЕР:{}\nТурнир:{}".format(
            id,
            self.players_storage[id].fio,
            self.players_storage[id].school,
            self.players_storage[id].year,
            self.players_storage[id].city,
            self.players_storage[id].region,
            self.players_storage[id].phone,
            self.players_storage[id].trainer,
            self.players_storage[id].tour
        )
    
    def set_unfixed(self, id):
        if not self.players_storage[id].fixed:
            return False, "Анкета итак не принята", ""
        self.players_storage[id].fixed = False
        self.players_storage[id].allowed = False
        return True, "Анкета вернулась учащемуся",  "<@{}> {}: Ваша анкета отвергнута".format(id, self.players_storage[id].fio)

    def allow(self, id, regg):
        if not self.players_storage[id].fixed:
            return False, "Анкета не принята", ""
        self.players_storage[id].allowed = True
        self.players_storage[id].user_id = id
        cursor = self.conn.cursor()
        entry = (self.players_storage[id].user_id, self.players_storage[id].tour, self.players_storage[id].fio, regg)
        cursor.execute("INSERT INTO players VALUES(?, ?, ?, ?);", entry)
        self.conn.commit()
        return True, "Игрок принят", "<@{}> {}: Ваша анкета принята".format(id, self.players_storage[id].fio)

    def admin_change_tour(self, id, new_tour):
        if not self.players_storage[id].allowed:
            return False, "Анкета не принята", ""
        cursor = self.conn.cursor()
        entry = (new_tour, id)
        cursor.execute("UPDATE players SET tour = ? WHERE user_id = ? ;", entry)
        self.conn.commit()
        self.players_storage[id].tour = new_tour
        return "True", "Турнир Сменен", "{}: Ваш турнир сменен на {}".format(self.players_storage[id].fio, new_tour)
