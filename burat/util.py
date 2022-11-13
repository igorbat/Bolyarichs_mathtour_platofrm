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
