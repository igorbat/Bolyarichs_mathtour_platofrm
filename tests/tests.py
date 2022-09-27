from random import randint
from PIL import ImageChops
from PIL import Image

from abaka import abaka_cls
from karusel import karusel_game, player, state_machine, team
import unittest


class TestSolveAbaka(unittest.TestCase):
    def get_player1(self):
        pl = abaka_cls.Player(1, "1s")
        return pl

    def get_1t(self):
        tour_1t = abaka_cls.GameAbaka("1t", "link", [["1", ["1"], ["1"]],
                                                     ["2", ["1"], ["1"]]])
        return tour_1t

    def test_solve(self):
        sm = abaka_cls.StateMachine()
        sm.register_player("1", "1")
        sm.add_tour("1t", self.get_1t())
        sm.start_tour("1t")
        sm.join_tour("1", "1t")
        sm.solve("1", "1", "1", "1")

        self.assertEqual(sm.players["1"].tours["1t"][4], 10)

        sm.solve("1", "1", "2", "1")

        self.assertEqual(sm.players["1"].tours["1t"][4], 10 + 20 + 50 * 2)

        sm.register_player("2", "1")
        sm.join_tour("2", "1t")
        sm.solve("2", "1", "1", "1")

        self.assertEqual(sm.players["2"].tours["1t"][4], 10)

        sm.solve("2", "1", "2", "1")

        self.assertEqual(sm.players["2"].tours["1t"][4], 10 + 20 + 50)

        sm.solve("2", "2", "1", "1")

        self.assertEqual(sm.players["2"].tours["1t"][4], 10 + 20 + 50 + 10 + 10 * 2)

        ok, msg = sm.solve("2", "2", "2", "1")

        self.assertEqual(sm.players["2"].tours["1t"][4], 10 + 20 + 50 + 10 + 10 * 2 + 20 + 50 * 2 + 20 * 2)
        self.assertEqual("Ответ совпал! Теперь у вас {}".format(10 + 20 + 50 + 10 + 10 * 2 + 20 + 50 * 2 + 20 * 2), msg)

    def test_sort(self):
        sm = abaka_cls.StateMachine()
        sm.register_player("1", "1")
        sm.register_player("2", "2")
        sm.register_player("3", "3")
        sm.add_tour("1t", abaka_cls.GameAbaka("1t", "link", [["1", ["1"], ["1"]], ["2", ["1"], ["1"]]]))
        sm.add_tour("2t", abaka_cls.GameAbaka("2t", "link", [["1", ["1"], ["1"]], ["2", ["1"], ["1"]]]))

        sm.start_tour("1t")
        sm.start_tour("2t")

        sm.join_tour("1", "2t")
        sm.join_tour("2", "2t")
        sm.join_tour("3", "2t")

        for player in sm.players.values():
            player.current_tour = None

        sm.join_tour("1", "1t")
        sm.join_tour("2", "1t")
        sm.join_tour("3", "1t")

        sm.solve("2", "2", "1", "1")
        sm.solve("1", "2", "1", "1")
        sm.solve("2", "1", "1", "1")
        sm.solve("1", "1", "1", "1")
        sm.solve("2", "2", "2", "2")

        vls = sm.get_sorted_res()
        for vll in vls:
            if vll[0] == "1t":
                self.assertEqual(vll[1][0][0], "2-1")
                self.assertEqual(vll[1][1][0], "1-1")
                self.assertEqual(vll[1][2][0], "3-1")
            if vll[0] == "2t":
                self.assertEqual(vll[1][0][0], "1-1")
                self.assertEqual(vll[1][1][0], "2-1")
                self.assertEqual(vll[1][2][0], "3-1")
        sm.reload_res()

    def test_table_sort(self):
        path_to_pic = '../tests/table_tests/expected_data/'
        tasks = [['theme' + str(j + 1), ["1"], ["1"], ["1"]] for j in range(3)]
        sm = abaka_cls.StateMachine()
        sm.register_player("super_good", "1")
        sm.register_player("super_bad", "2")
        sm.register_player("almost_afk", "3")
        sm.register_player("bonus_hunter", "4")
        sm.register_player("normal_student", "5")
        sm.add_tour("1t", abaka_cls.GameAbaka("1t", "link", tasks))

        sm.start_tour("1t")

        sm.join_tour("super_good", "1t")
        sm.join_tour("super_bad", "1t")
        sm.join_tour("almost_afk", "1t")
        sm.join_tour("bonus_hunter", "1t")
        sm.join_tour("normal_student", "1t")

        sm.solve("almost_afk", "theme2", "1", "2")
        sm.solve("bonus_hunter", "theme1", "1", "1")
        sm.solve("bonus_hunter", "theme3", "1", "1")
        sm.solve("normal_student", "theme1", "1", "1")
        sm.solve("normal_student", "theme2", "1", "1")
        sm.solve("super_good", "theme1", "1", "1")
        sm.solve("super_bad", "theme3", "1", "2")
        sm.solve("bonus_hunter", "theme2", "1", "1")
        sm.solve("super_good", "theme1", "2", "1")
        sm.solve("super_bad", "theme3", "2", "2")
        sm.solve("normal_student", "theme2", "2", "1")
        sm.solve("super_bad", "theme1", "1", "2")
        sm.solve("super_bad", "theme2", "1", "2")
        sm.solve("normal_student", "theme1", "2", "1")
        sm.solve("super_good", "theme2", "1", "1")
        sm.solve("bonus_hunter", "theme3", "2", "2")
        sm.solve("normal_student", "theme3", "1", "1")
        sm.solve("bonus_hunter", "theme2", "2", "1")
        sm.solve("super_good", "theme2", "2", "1")
        sm.solve("super_bad", "theme1", "2", "2")
        sm.solve("almost_afk", "theme3", "1", "1")
        sm.solve("normal_student", "theme3", "1", "2")
        sm.solve("bonus_hunter", "theme1", "2", "1")
        sm.solve("super_good", "theme3", "1", "1")
        sm.solve("bonus_hunter", "theme2", "3", "1")
        sm.solve("super_good", "theme2", "3", "1")
        sm.solve("super_good", "theme1", "3", "1")
        sm.solve("normal_student", "theme2", "3", "2")

        sm.res_table("super_good", fnt_size=32, path_to_pic=path_to_pic + "super_good_table.png")
        sm.res_table("super_bad", path_to_pic=path_to_pic + "super_bad_table.png")
        sm.res_table("almost_afk", path_to_pic=path_to_pic + "almost_afk_table.png")
        sm.res_table("bonus_hunter", path_to_pic=path_to_pic + "bonus_hunter_table.png")
        sm.res_table("normal_student", path_to_pic=path_to_pic + "normal_student_table.png")

        with Image.open(path_to_pic + "super_good_table.png") as im:
            print(self.compare_pics(im, im))

    def compare_pics(self, pic1, pic2):
        diff = ImageChops.difference(pic1, pic2)
        if diff.getbbox():
            return False
        else:
            return True

class TestSolveKarusel(unittest.TestCase):
    def get_player1(self):
        pl = player.Player("id_of_the_player")
        return pl

    def get_1t(self):
        game = karusel_game.GameKarusel("test", "link", ['1', '0', '0', '5', '0', '0'])
        return game

    def test_solve(self):
        sm = state_machine.StateMachine()
        sm.register_player("1", "1")
        sm.add_tour("1t", self.get_1t())

        sm.start_tour("1t")

        sm.join_tour("1", "1t")
        sm.solve("1", "1")

        self.assertEqual(sm.players["1"].team.total_points, 3)

        sm.solve("1", "0")

        self.assertEqual(sm.players["1"].team.total_points, 7)

        sm.register_player("2", "1")
        sm.join_tour("2", "1t")
        sm.solve('2', '1')

        self.assertEqual(sm.players["2"].team.total_points, 3)

        sm.solve("2", "1")

        self.assertEqual(sm.players["2"].team.total_points, 3)

        sm.solve("2", '0')

        self.assertEqual(sm.players["2"].team.total_points, 6)

        ok, msg = sm.solve("2", "5")

        self.assertEqual(sm.players["2"].team.total_points, 10)

    def test_sort(self):
        pass


# ts_karusel = TestSolveKarusel()
# ts_karusel.test_solve()
# ts_karusel.test_sort()

ts_abaka = TestSolveAbaka()
# ts_abaka.test_solve()
ts_abaka.test_table_sort()
