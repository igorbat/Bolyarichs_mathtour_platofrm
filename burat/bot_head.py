from util import calculate_points, generate_html, generate_html_bonuses
from solution_cache import SolutionCache
from task_cache import TaskCache
from player_cache import PlayerCache

# TODO: every command should return something
class Father:
    def __init__(self):
        self.solutions = SolutionCache()
        self.players = PlayerCache()
        self.tasks = TaskCache()

    def registered(self, v1, v2):
        return self.players.allow(v1, v2)
    
    def banned(self, v1):
        return self.players.set_unfixed(v1)
    
    def changetour(self, v1, v2):
        return self.players.admin_change_tour(v1, v2)
    
    def newtasks(self, v1, v2, v3, v4, v5, v6, v7):
        return self.tasks.create_or_update_task(v1, v2, v3, v4, v5, v6, v7)
    
    def finish(self):
        self.solutions.conn.close()
        self.players.conn.close()
        self.tasks.conn.close()
    
    def res_res_res(self):
        generate_html(self.solutions, self.tasks, self.players)
    
    def super_res(self):
        generate_html_bonuses(self.solutions, self.tasks, self.players)
    
    def solve(self, idd, v1, v2, v3):
        if not self.players.players_storage[idd].allowed:
            msg = "Вы еще не зарегистрированы"
            return msg
        tour = self.players.players_storage[idd].tour
        ok_, msgg = self.tasks.is_task(tour, v1, v2, v3)
        if not ok_:
            return msgg
        # проверить, что не было повторной посылки по той же задаче
        theme_count = 0
        for sol in self.solutions.solution_storage:
            if sol[0] == idd and sol[1] == v1:
                theme_count += 1
        if theme_count + 1 > int(v2):
            return "Вы уже отправляли данную задачу"
        elif theme_count + 1 < int(v2):
            return "Вы ещё не отправили прошлые задачи"
            

        ok, msg1 = self.solutions.new_solution(idd, v1, v2, v3)
        # print(msg1)
        ok2 = self.tasks.check_task(tour,  v1, v2, v3)
        return msg1 + '\n' + "Ура! ответ совпал с текущим в базе" if ok2 else "Увы, ответ не совпал с текущим в базе"
    
    def points(self, idd):
        if not self.players.players_storage[idd].allowed:
            msg = "Вы еще не зарегистрированы"
            return msg
        tour = self.players.players_storage[idd].tour
        ok, msg = calculate_points(idd, tour, self.solutions, self.tasks)
        return msg
    
    def fio(self, idd, v1):
        return self.players.set_fio(idd, v1)

    def school(self, idd, v1):
        return self.players.set_school(idd, v1)

    def year(self, idd, v1):
        return self.players.set_year(idd, v1)

    def city(self, idd, v1):
        return self.players.set_city(idd, v1)

    def region(self, idd, v1):
        return self.players.set_region(idd, v1)

    def phone(self, idd, v1):
        return self.players.set_phone(idd, v1)

    def trainer(self, idd, v1):
        return self.players.set_trainer(idd, v1)
    
    def tour(self, idd, v1):
        return self.players.set_tour(idd, v1)
    
    def register(self, idd):
        return self.players.set_fixed(idd)





father = Father()