from burat.solution_cache import SolutionCache
from burat.task_cache import TaskCache


def calculate_points(player, tour, solution_cache: SolutionCache, tasks_cache: TaskCache):
    # player <=> user_id
    points = 0
    for sol in solution_cache.solution_storage:
        if sol[0] == player:
            if tasks_cache.check_task(tour, sol[1], sol[2], sol[3]):
                points += int(sol[2]) * 10
    return (True, f'Ваше число очков: {points}')