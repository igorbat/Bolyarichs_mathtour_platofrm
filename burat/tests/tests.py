from player_cache import PlayerCache
from solution_cache import SolutionCache
from secret import DB_NAME

import unittest

from task_cache import TaskCache


class CacheTest(unittest.TestCase):
    def solution_cache_test(self, print_ok=True):
        # грохает базу (очищает файл)
        open(DB_NAME, 'w').close()
        sols = []
        sol_c1 = SolutionCache(DB_NAME)

        sol_c1.new_solution('1', 'algebra', '1', '2.45')
        sol_c1.new_solution('1', 'geometry', '1', '45')
        sol_c1.new_solution('2', 'combinatorics', '2', 'yes')
        sol_c1.new_solution('3', 'topology', '1', 'bibki')
        sol_c1.new_solution('2', 'algebra', '2', '2.718')

        for i in range(5):
            sols.append(sol_c1.solution_storage[i])
        sol_c1.conn.close()

        sol_c2 = SolutionCache(DB_NAME)
        for i in range(5):
            for j in range(4):
                if sol_c2.solution_storage[i][j] != sols[i][j]:
                    print("Не совпали значения с такими координатами: ", str(i) + ',', j)
                    sol_c2.conn.close()
                    return False
        if print_ok:
            print('solutions is ok')
        sol_c2.conn.close()

    def compare_task_cache_and_db(self, tasks, groups):
        task_c2 = TaskCache(DB_NAME)
        c = 0
        for group in groups:
            for theme in task_c2.tours[group]:
                if str(tasks[c]) != str(task_c2.tours[group][theme]):
                    print("Не совпали значения с такими координатами: ", str(group) + ',', theme)
                    task_c2.conn.close()
                    return False
                c += 1
        task_c2.conn.close()
        return True

    def task_cache_test_create(self, print_ok=True):
        open(DB_NAME, 'w').close()
        tasks = []
        groups = ["pro", "novice"]
        task_c1 = TaskCache(DB_NAME)

        task_c1.new_task("pro", '1', '0', '0', '0', '0', '0')
        task_c1.new_task("pro", '2', 'a', 'a', 'a', 'a', 'a')
        task_c1.new_task("pro", '3', 'biba', 'boba', 'pupa', 'lupa', 'shushunchik')
        task_c1.new_task("novice", '4', 'yes', 'no', 'no', 'yes', 'yes')
        task_c1.new_task("novice", '5', 'no', 'no', 'maybe', 'yes', 'yes')

        for group in groups:
            for theme in task_c1.tours[group]:
                tasks.append(task_c1.tours[group][theme])
        task_c1.conn.close()

        if self.compare_task_cache_and_db(tasks, groups) and print_ok:
            print("task creating is ok")

    def task_cache_test_update(self, print_ok=True):
        self.task_cache_test_create(False)
        tasks = []
        groups = ["pro", "novice"]
        task_c1 = TaskCache(DB_NAME)

        task_c1.update_task("pro", '1', '1', '2', '3', '4', '5')
        task_c1.update_task("pro", '2', '-1', '-2', '-3', '-4', '-5')
        task_c1.update_task("pro", '3', '1.0', '2.0', '3.0', '4.0', '5.0')
        task_c1.update_task("novice", '4', '1e', '2e', '3e', '4e', '5e')
        task_c1.update_task("novice", '5', 'a', 'b', 'c', 'd', 'e')

        for group in groups:
            for theme in task_c1.tours[group]:
                tasks.append(task_c1.tours[group][theme])
        task_c1.conn.close()

        if self.compare_task_cache_and_db(tasks, groups) and print_ok:
            print("task updating is ok")

    def task_cache_test_create_or_update(self, print_ok=True):
        self.task_cache_test_create(False)
        tasks = []
        groups = ["pro", "novice"]
        task_c1 = TaskCache(DB_NAME)

        task_c1.create_or_update_task("pro", '1', '1', '2', '3', '4', '5')
        task_c1.create_or_update_task("pro", '2', '-1', '-2', '-3', '-4', '-5')
        task_c1.create_or_update_task("pro", '6', '1.0', '2.0', '3.0', '4.0', '5.0')
        task_c1.create_or_update_task("novice", '4', '1e', '2e', '3e', '4e', '5e')
        task_c1.create_or_update_task("novice", '7', 'a', 'b', 'c', 'd', 'e')

        for group in groups:
            for theme in task_c1.tours[group]:
                tasks.append(task_c1.tours[group][theme])
        task_c1.conn.close()

        if self.compare_task_cache_and_db(tasks, groups) and print_ok:
            print("task creating or updating is ok")

    def player_cache_test(self):
        open(DB_NAME, 'w').close()
        player_c1 = PlayerCache()
        # функций для проеверки пока нет


cache_test = CacheTest()
cache_test.solution_cache_test()
cache_test.task_cache_test_create()
cache_test.task_cache_test_update()
cache_test.task_cache_test_create_or_update()
