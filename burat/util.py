from solution_cache import SolutionCache
from task_cache import TaskCache
from collections import defaultdict
import codecs


def calculate_points(player, tour, solution_cache: SolutionCache, tasks_cache: TaskCache):
    # player <=> user_id
    points = 0
    for sol in solution_cache.solution_storage:
        if sol[0] == player:
            if tasks_cache.check_task(tour, sol[1], sol[2], sol[3]):
                points += int(sol[2]) * 10
    return (True, f'Ваше число очков: {points}')


def generate_html(solutions, tasks, players):
    results = defaultdict(list)
    for playerr in players.players_storage:
        player = players.players_storage[playerr]
        if not player.allowed:
            continue
        tour = player.tour
        fio = player.fio
        fio = fio.replace('\n', ', ')
        points = 0
        sols = 0
        corrects_sols = 0
        for sol in solutions.solution_storage:
            if sol[0] == player.user_id:
                sols += 1
                if tasks.check_task(tour, sol[1], sol[2], sol[3]):
                    points += int(sol[2]) * 10
                    corrects_sols += 1
        results[tour].append([fio, points, corrects_sols, sols])

    for tour in results:
        sorted_res = sorted(results[tour], key=lambda x: -x[1])
        with codecs.open(tour + '_res.html', 'w', "utf-8") as f:
            f.write("<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\"><title>{}</title></head>\n<body>".format(tour))
            f.write("<div>очков задач посылок место название </div>")
            for _, mass in enumerate(sorted_res):
                f.write("<div><pre>" + str(mass[1]).ljust(6, " ") + str(mass[2]).ljust(6, " ") +
                        str(mass[3]).ljust(8, " ") + str(_ + 1).ljust(6, " ") + mass[0] + "</pre></div>")
            f.write("</body></html>")


def generate_html_bonuses(solutions, tasks, players):
    player_results = defaultdict(list)
    for playerr in players.players_storage:
        player = players.players_storage[playerr]
        if not player.allowed:
            continue
        tour = player.tour
        fio = player.fio
        fio = fio.replace('\n', ', ')
        if tour == "pro":
            mapp = []
            for i in range(4):
                mapp.append([0, 0, 0, 0, 0])
        else:
            mapp = []
            for i in range(7):
                mapp.append([0, 0, 0, 0, 0])
        
        player_results[player.user_id] = [fio, 0, 0, 0, tour, mapp]
    
    mapper = {
        "pro":
            {
                "move1":0,
                "alg1":1,
                "chisl1":2,
            },
        "novice":
            {
                "num1":0,
                "razn1":1,
                "dir":2,
            }
    }
    uniq_bonuses = {
        "pro":
            {
                "move1":0,
                "alg1":0,
                "chisl1":0,
                1:0,
                2:0,
                3:0,
                4:0,
                5:0
            },
        "novice":
            {
                "num1":0,
                "razn1":0,
                "dir":0,
                1:0,
                2:0,
                3:0,
                4:0,
                5:0
            }
    }
    for sol in solutions.solution_storage:
        player_results[sol[0]][3] += 1
        if tasks.check_task(player_results[sol[0]][4], sol[1], sol[2], sol[3]):
            player_results[sol[0]][1] += int(sol[2]) * 10
            player_results[sol[0]][2] += 1
            player_results[sol[0]][5][mapper[player_results[sol[0]][4]][sol[1]]][int(sol[2]) - 1] = 1

            sum_theme = sum(player_results[sol[0]][5][mapper[player_results[sol[0]][4]][sol[1]]])
            sum_number = 0
            for theme in player_results[sol[0]][5]:
                sum_number += theme[int(sol[2]) - 1]
            
            if sum_theme == 5:
                player_results[sol[0]][1] += 50
                print("Player {} took bonus in theme: {}".format(sol[0] + player_results[sol[0]][0], sol[1]))
                if uniq_bonuses[player_results[sol[0]][4]][sol[1]] == 0:
                    player_results[sol[0]][1] += 50
                    print("Player {} took first bonus in theme: {}".format(sol[0] + player_results[sol[0]][0], sol[1]))
                    uniq_bonuses[player_results[sol[0]][4]][sol[1]] = 1
            
            if sum_number == len(mapper[player_results[sol[0]][4]]):
                player_results[sol[0]][1] += int(sol[2]) * 10
                print("Player {} took bonus in theme: {}, tour = {}".format(sol[0] + player_results[sol[0]][0], sol[2], player_results[sol[0]][4]))
                if uniq_bonuses[player_results[sol[0]][4]][int(sol[2])] == 0:
                    player_results[sol[0]][1] += int(sol[2]) * 10
                    print("Player {} took first bonus in theme: {}, tour = {}".format(sol[0] + player_results[sol[0]][0], sol[2], player_results[sol[0]][4]))
                    uniq_bonuses[player_results[sol[0]][4]][int(sol[2])] = 1
    
    results = defaultdict(list)
    for playert in player_results:
        player = player_results[playert]
        results[player[4]].append([player[0], player[1], player[2], player[3]])

    for tour in results:
        sorted_res = sorted(results[tour], key=lambda x: -x[1])
        with codecs.open(tour + '_res_bonuses.html', 'w', "utf-8") as f:
            f.write("<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\"><title>{}</title></head>\n<body>".format(tour))
            f.write("<div>очков задач посылок место название </div>")
            for _, mass in enumerate(sorted_res):
                if mass[3] > 0:
                    f.write("<div><pre>" + str(mass[1]).ljust(6, " ") + str(mass[2]).ljust(6, " ") +
                            str(mass[3]).ljust(8, " ") + str(_ + 1).ljust(6, " ") + mass[0] + "</pre></div>")
            f.write("</body></html>")
