from collections import defaultdict

from burat.player_cache import PlayerCache
from burat.solution_cache import SolutionCache
from burat.task_cache import TaskCache
from burat.graphic_environment.table_drawer import TableDrawer
from burat.util import calculate_points
from burat.data.conf import TABLE_NAME, PATH


def table_from_cache(player, player_cache: PlayerCache, solution_cache: SolutionCache, tasks_cache: TaskCache, font_size=32, path_to_pic=None):
    # player <=> user_id
    double_cells = [[0, 0, 'Темы', '№ Задач']]
    theme_ind = 1
    tour = player_cache.players_storage[player].tour
    board = [['' for i in range(6)] for j in range(len(tasks_cache.tours[tour]) + 1)]
    board[0][0] = ' '
    theme_to_ind = defaultdict()
    for theme in tasks_cache.tours[tour]:
        theme_to_ind[theme] = theme_ind
        theme_ind += 1
    for theme in theme_to_ind:
        board[theme_to_ind[theme]][0] = theme
    for i in range(1, 6):
        board[0][i] = str(i)
    solutions = []
    for sol in solution_cache.solution_storage:
        if sol[0] == player:
            solutions.append(sol)
    for sol in solutions:
        if tasks_cache.check_task(tour, sol[1], sol[2], sol[3]):
            board[theme_to_ind[sol[1]]][int(sol[2])] = int(sol[2]) * 10
        else:
            board[theme_to_ind[sol[1]]][int(sol[2])] = 0

    if path_to_pic is None:
        path_to_pic = PATH + TABLE_NAME
    path = TableDrawer.draw_table(board, font_size, path_to_pic, color_matrix='default', double_cells=double_cells)
    points = calculate_points(player, tour, solution_cache, tasks_cache)
    return path, TABLE_NAME, points