from solution_cache import SolutionCache
from task_cache import TaskCache
from collections import defaultdict
import codecs


def calculate_points(
    player, tour, solution_cache: SolutionCache, tasks_cache: TaskCache
):
    sol_data = {}  # (num1, num2) -> count of tries
    # solution is [user_id, name, answer, time] where name is num1num2
    # player <=> user_id
    points = 0
    for sol in solution_cache.solution_storage:
        num1, num2 = int(sol[1][0]), int(sol[1][1])
        if num1 > num2:
            num1, num2 = num2, num1
        print(sol)
        if sol[0] == player:
            if tasks_cache.check_task(tour, num1, num2, sol[2]):
                if (num1, num2) not in sol_data:
                    points += num1 + num2 if num1 + num2 != 0 else 10
                else:
                    points += num2
            else:
                if (num1, num2) in sol_data:
                    points -= num1
            sol_data[(num1, num2)] = 1

    return (True, f"Ваше число очков: {points}")


def get_sols_info(player, tour, solution_cache: SolutionCache, tasks_cache: TaskCache):
    sol_data = {}  # (num1, num2) -> count of tries
    # solution is [user_id, name, answer, time] where name is num1num2
    # player <=> user_id
    points = 0
    sols = 0
    corrects_sols = 0
    for sol in solution_cache.solution_storage:
        num1, num2 = int(sol[1][0]), int(sol[1][1])
        if num1 > num2:
            num1, num2 = num2, num1
        print(sol)
        if sol[0] == player:
            sols += 1
            if tasks_cache.check_task(tour, num1, num2, sol[2]):
                corrects_sols += 1
                if (num1, num2) not in sol_data:
                    points += num1 + num2 if num1 + num2 != 0 else 10
                else:
                    points += num2
            else:
                if (num1, num2) in sol_data:
                    points -= num1
            sol_data[(num1, num2)] = 1
    return [points, sols, corrects_sols]


def generate_html(solutions, tasks, players):
    results = defaultdict(list)
    for playerr in players.players_storage:
        print(playerr)
        player = players.players_storage[playerr]
        if not player.allowed:
            continue
        tour = player.tour
        fio = player.fio
        fio = fio.replace("\n", ", ")
        points, sols, corrects_sols = get_sols_info(
            str(playerr), tour, solutions, tasks
        )

        results[tour].append([fio, points, corrects_sols, sols])

    for tour in results:
        sorted_res = sorted(results[tour], key=lambda x: -x[1])
        with codecs.open(tour + "_res.html", "w", "utf-8") as f:
            f.write(
                '<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>{}</title></head>\n<body>'.format(
                    tour
                )
            )
            f.write("<div>очков задач посылок место название </div>")
            for _, mass in enumerate(sorted_res):
                f.write(
                    "<div><pre>"
                    + str(mass[1]).ljust(6, " ")
                    + str(mass[2]).ljust(6, " ")
                    + str(mass[3]).ljust(8, " ")
                    + str(_ + 1).ljust(6, " ")
                    + mass[0]
                    + "</pre></div>"
                )
            f.write("</body></html>")
