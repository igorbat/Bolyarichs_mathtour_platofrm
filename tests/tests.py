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
        sm.join_tour("1", "1t")
        sm.solve("1", "1")

        self.assertEqual(sm.players["1"].team.total_points, 3)

        sm.solve("1", "0")

        self.assertEqual(sm.players["1"].team.total_points, 9)

        sm.register_player("2", "1")
        sm.join_tour("2", "1t")
        sm.solve('2', '1')

        self.assertEqual(sm.players["2"].team.total_points, 3)

        sm.solve("2", "1")

        self.assertEqual(sm.players["2"].team.total_points, 3)

        sm.solve("2", '0')

        self.assertEqual(sm.players["2"].team.total_points, 6)

        ok, msg = sm.solve("2", "5")

        self.assertEqual(sm.players["2"].team.total_points, 12)

    def test_sort(self):
            pass


ts = TestSolveKarusel()
ts.test_solve()
ts.test_sort()
