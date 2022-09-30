from abaka.conf import PATH, TABLE_NAME
from graphic_environment.table_drawer import TableDrawer
from collections import defaultdict
import codecs
import os

class Player:
    def __init__(self, acc_id, team_name):
        self.acc_id = acc_id
        self.team_name = team_name
        self.tours = {}
        self.current_tour = None
        self.gotten_bonuses = []

    def join_tour(self, tour, tour_info):
        # if self.current_tour is None:
        self.current_tour = tour
        if tour not in self.tours:
            self.tours[tour] = [list(tour_info[:-1])[0], tour_info[-1], [], [], 0]
            # themes
            # task number
            # sent tasks
            # success tasks
            # points
        return True, "Успех. Ваш текущий турнир {}".format(self.current_tour)

        # return False, "Вы уже играете в турнире {}".format(self.current_tour)

    def leave_tour(self):
        self.current_tour = None

    def can_try_solve_task(self, theme, idd):
        if self.current_tour is None:
            return (False, "нет никакого турнира, в котором бы вы играли")

        if theme not in self.tours[self.current_tour][0]:
            return (False, "такой темы нет")

        code = theme + "_" + idd
        if code in self.tours[self.current_tour][2]:
            return (False, "Вы уже отправляли такую задачу")
        try:
            if 0 < int(idd) <= self.tours[self.current_tour][1]:
                ok = True
            else:
                ok = False
        except:
            return (False, "что-то не так с айди задачи")

        if ok:
            ddq = int(idd)
            for i in range(1, ddq):
                code_2 = theme + "_" + str(i)
                if code_2 not in self.tours[self.current_tour][2]:
                    return (False, "Вы не отправили задачу {}".format(i))
            return (ok, "")
        else:
            return (False, "что-то не так с айди задачи")

    def add_solution(self, theme, idd, is_success):
        self.tours[self.current_tour][2].append(theme + "_" + idd)
        if is_success:
            self.tours[self.current_tour][4] += int(idd) * 10
            self.tours[self.current_tour][3].append(theme + "_" + idd)

    def check_bonuses(self, theme, idd):
        bonuses_lst = []
        ok = True
        for i in range(self.tours[self.current_tour][1]):
            ok = ok and ((theme + "_" + str(i + 1)) in self.tours[self.current_tour][3])
        if ok:
            bonuses_lst.append(theme)
        ok = True
        for themee in self.tours[self.current_tour][0]:
            ok = ok and ((themee + "_" + idd) in self.tours[self.current_tour][3])
        if ok:
            bonuses_lst.append(int(idd))
        return bonuses_lst

    def add_bonus(self, p):
        self.tours[self.current_tour][4] += p

    def add_bonus_type(self, b_type):
        if b_type not in self.gotten_bonuses:
            self.gotten_bonuses.append(b_type)

    def sent_tasks(self):
        if self.current_tour is None:
            return (False, "нет никакого турнира, в котором бы вы играли")
        return (True, self.tours[self.current_tour][2])

    def my_point(self):
        if self.current_tour is None:
            return (False, "нет никакого турнира, в котором бы вы играли")
        return (True, self.tours[self.current_tour][4])


class GameAbaka:
    def __init__(self, name, link, tasks):
        self.name = name
        self.link = link
        self.themes = [tsk_line[0] for tsk_line in tasks]
        self.task_count = len(tasks[0]) - 1
        self.bonuses = set([theme for theme in self.themes] + [i for i in range(1, self.task_count + 1)])
        self.bonus_to_point = {}
        for bonus in self.bonuses:
            if bonus in self.themes:
                self.bonus_to_point[bonus] = 50
            else:
                self.bonus_to_point[bonus] = bonus * 10
        self.taken_bonuses = set()
        self.solutions = {}
        for tsk_line in tasks:
            theme = tsk_line[0]
            idd = 1
            for sol in tsk_line[1:]:
                self.solutions[theme + "_" + str(idd)] = sol
                idd += 1

        self.active = False

    def get_name(self):
        return self.name

    def get_tour_info(self):
        return (self.themes, self.task_count)

    def start(self):
        self.active = True
        return (True, "Игра началась")

    def stop(self):
        self.active = False
        return (True, "Игра отключена")

    def get_tasks(self):
        return self.link

    def try_solve_task(self, theme, idd,  res):
        code = theme+ "_" + idd
        if code not in self.solutions:
            return (False, False, "Или темы нет, или такого номера нет")
        else:
            if res not in self.solutions[code]:
                return (True, False, "Не нашел совпадающего ответа")
            else:
                return (True, True, "Ответ совпал!")

    def get_bonus(self, bonus_type):
        if bonus_type in self.bonuses and bonus_type not in self.taken_bonuses:
            self.taken_bonuses.add(bonus_type)
            return self.bonus_to_point[bonus_type] * 2
        return self.bonus_to_point[bonus_type]

    def multiplier_check(self, bonus_type):
        if bonus_type in self.bonuses and bonus_type not in self.taken_bonuses:
            return '2'
        return '1'


class StateMachine:
    def __init__(self):
        self.players = {}
        self.tours = {}
        self.teams = {}

    def add_tour(self, tour_name, game):
        self.tours[tour_name] = game

    def start_tour(self, tour_name):
        if tour_name not in self.tours:
            return (False, "Нет такого турнира")

        ok, msg = self.tours[tour_name].start()
        return ok, msg

    def stop_tour(self, tour_name):
        if tour_name not in self.tours:
            return (False, "Нет такого турнира")

        ok, msg = self.tours[tour_name].stop()
        return ok, msg

    def register_player(self, player_id, team_name):
        if player_id in self.players:
            return "У вас уже есть команда: {}".format(self.players[player_id].team_name)

        if team_name not in self.teams:
            self.teams[team_name] = 1
            idd = 1
        else:
            self.teams[team_name] += 1
            idd = self.teams[team_name]

        tm = team_name + "-" + str(idd)
        self.players[player_id] = Player(player_id, tm)
        return tm

    def join_tour(self, player_id, tour_name):
        if tour_name not in self.tours:
            return (False, "Нет такого турнира")

        if player_id not in self.players:
            return (False, "Нет такого игрока")

        if not self.tours[tour_name].active:
            return (False, "Турник отключен")
        ok, msg = self.players[player_id].join_tour(tour_name, self.tours[tour_name].get_tour_info())
        return ok, msg

    def solve(self, player_id, *parts):
        if player_id not in self.players:
            return False, "Нет такого игрока"

        if len(parts) != 3:
            return False, "Неверный формат ответа. Решение должно быть в виде 'solve ТЕМА ЗАДАЧА ОТВЕТ'"

        theme, idd, sol = parts

        ok, msg = self.players[player_id].can_try_solve_task(theme, idd)
        if not ok:
            return ok, msg

        if not self.tours[self.players[player_id].current_tour].active:
            return (False, "Турник отключен")

        ok, status, msg = self.tours[self.players[player_id].current_tour].try_solve_task(theme, idd, sol)
        if not ok:
            return ok, msg

        self.players[player_id].add_solution(theme, idd, status)
        if status:
            bns_lst = self.players[player_id].check_bonuses(theme, idd)
            for bns in bns_lst:
                multiplier = self.tours[self.players[player_id].current_tour].multiplier_check(bns)
                self.players[player_id].add_bonus_type(str(bns) + '_' + multiplier)
                p = self.tours[self.players[player_id].current_tour].get_bonus(bns)
                self.players[player_id].add_bonus(p)

        ok, new_p = self.players[player_id].my_point()
        return True, msg + " Теперь у вас {}".format(new_p)

    def tasks(self, player_id):
        if player_id not in self.players:
            return (False, "Нет такого игрока")
        if self.players[player_id].current_tour is None:
            return (False, "Вы нигде не играете")
        if not self.tours[self.players[player_id].current_tour].active:
            return (False, "Турник отключен")
        return (True, self.tours[self.players[player_id].current_tour].get_tasks())

    def sent_task(self, player_id):
        if player_id not in self.players:
            return (False, "Нет такого игрока")
        if self.players[player_id].current_tour is None:
            return (False, "Вы нигде не играете")
        if not self.tours[self.players[player_id].current_tour].active:
            return (False, "Турник отключен")
        return (True, self.tours[self.players[player_id].current_tour].sent_tasks())

    def points(self, player_id):
        if player_id not in self.players:
            return (False, "Нет такого игрока")
        ok, msg = self.players[player_id].my_point()
        return (ok, msg)

    # TODO слишком много строк, разделить на подфункции
    def res_table(self, player_id, fnt_size=32, path_to_pic=None):
        if player_id not in self.players:
            return (False, "Нет такого игрока")
        if self.players[player_id].current_tour is None:
            return (False, "Вы нигде не играете")
        if not self.tours[self.players[player_id].current_tour].active:
            return (False, "Турник отключен")
        tour = self.tours[self.players[player_id].current_tour]
        x_size = len(tour.themes)
        y_size = tour.task_count
        themes = {}
        for x in range(x_size):
            themes[tour.themes[x]] = x + 1
        failed_tasks = self.players[player_id].tours[tour.name][2]
        successful_tasks = self.players[player_id].tours[tour.name][3]
        points = self.players[player_id].my_point()[1]
        gotten_bonuses = self.players[player_id].gotten_bonuses
        board = [['' for i in range(y_size + 2)] for j in range(x_size + 2)]
        color_matrix = [['' for i in range(y_size + 2)] for j in range(x_size + 2)]
        white = (255, 255, 255)
        yellow = (254, 242, 80)
        double_cells = [[0, 0, 'Темы', '№ Задач']]

        # fills names of themes and tasks
        color_matrix[0][0] = white
        color_matrix[x_size + 1][y_size + 1] = white
        for x in range(1, x_size + 1):
            board[x][0] = tour.themes[x - 1]
            color_matrix[x][0] = white
        for y in range(1, y_size + 1):
            board[0][y] = str(y)
            color_matrix[0][y] = white

        # add bonuses to bottom and right cells
        board[x_size + 1][0] = 'Бонус'
        board[0][y_size + 1] = 'Бонус'
        color_matrix[x_size + 1][0] = white
        color_matrix[0][y_size + 1] = white

        # add total to the most bottom-right cell !NOT IMPLEMENTED!

        # fill board with points without bonuses and matrices
        for f_task in failed_tasks:
            theme, idd = f_task.split('_')
            theme_ind = themes[theme]
            idd_ind = int(idd)
            board[theme_ind][idd_ind] = 0
            color_matrix[theme_ind][idd_ind] = 'red'
        for s_task in successful_tasks:
            theme, idd = s_task.split('_')
            theme_ind = themes[theme]
            idd_ind = int(idd)
            board[theme_ind][idd_ind] = idd_ind * 10
            color_matrix[theme_ind][idd_ind] = 'green'

        # fills bonus cells
        for bonus in gotten_bonuses:
            bns_type, mult_str = bonus.split('_')
            mult = int(mult_str)
            if not bns_type.isnumeric():
                board[themes[bns_type]][y_size + 1] = 50 * mult
                if mult == 2:
                    color_matrix[themes[bns_type]][y_size + 1] = yellow
                else:
                    color_matrix[themes[bns_type]][y_size + 1] = 'green'
            else:
                column = int(bns_type)
                board[x_size + 1][column] = column * 10 * mult
                if mult == 2:
                    color_matrix[x_size + 1][column] = yellow
                else:
                    color_matrix[x_size + 1][column] = 'green'

        if path_to_pic is None:
            path_to_pic = PATH + TABLE_NAME
        return TableDrawer.draw_table(board, fnt_size, path_to_pic, color_matrix, double_cells, points)

    def get_sorted_res(self):
        tour_names = self.tours.keys()
        tours = defaultdict(list)
        for tour_name in tour_names:
            for player in self.players.values():
                if tour_name in player.tours:
                    tours[tour_name].append([
                        player.team_name,
                        player.tours[tour_name][4],  # points
                        player.tours[tour_name][3],  # success
                        player.tours[tour_name][2]  # sent_amount                    ,
                    ])
        res = []
        for tour_name in tour_names:
            res.append([])
            res[-1].append(tour_name)
            qwes = sorted(tours[tour_name], key=lambda x: (-x[1], len(x[2]), -len(x[3]), x[0]))
            res[-1].append(qwes)
        return res

    def reload_res(self):
        sorted_res = self.get_sorted_res()

        for v in sorted_res:
            name, mas = v
            with codecs.open(name + '_res.html', 'w', "utf-8") as f:
                f.write("<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\"><title>{}</title></head>\n<body>".format(name))
                f.write("<div>очков задач посылок место название </div>")
                for _, mass in enumerate(mas):
                    f.write("<div><pre>" + str(mass[1]).ljust(6, " ") + str(len(mass[2])).ljust(6, " ") +
                            str(len(mass[3])).ljust(8, " ") + str(_ + 1).ljust(6, " ") + mass[0] + "</pre></div>")
                excess_bonuses = [bns for bns in self.tours[name].bonuses if bns not in self.tours[name].taken_bonuses]
                f.write("<div><pre>Оставшиеся первые бонусы для всех! {}</pre></div>".format(excess_bonuses))
                f.write("</body></html>")

    def get_text_res(self):
        sorted_res = self.get_sorted_res()

        msg = ''
        for v in sorted_res:
            name, mas = v
            msg += 'ТУРНИР ' + name + '\n'
            msg = 'очков задач посылок место название\n'
            for _, mass in enumerate(mas):
                msg += \
                    str(mass[1]).ljust(6, " ") + str(len(mass[2])).ljust(6, " ") +\
                    str(len(mass[3])).ljust(8, " ") + str(_ + 1).ljust(6, " ") + mass[0] + "\n"
                excess_bonuses = [bns for bns in self.tours[name].bonuses if bns not in self.tours[name].taken_bonuses]
                msg += 'Оставшиеся первые бонусы для всех! {}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'.format(excess_bonuses)

        return (True, msg)
