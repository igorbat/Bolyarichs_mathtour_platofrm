class Team:
    """
    Class representing a group of people who participate in a tour
    Attributes:
        self.team_name - name of the team
        self.active_tour - game which team is playing right now
        self.players - list of players who join that team
        self.problem_number - index of current problem that team has to solve now
        self.cur_reward - reward that the team will get in case they solve the next task correctly
        self.total_points - total amount of points that the team has earned
        self.given_answers - list of given answers

    Methods:
        self.start_game(game: GameKarusel) -> (status: bool, message: str) - sets the active tour of the team.
        In case if active tour is not None, gives the corresponding result
        self.sent_tasks() -> str - returns the string representing the answers that team has given
        self.get_points() -> (status: bool, points: int) - returns current amount of points that team has
        self.solve(ans: str) -> (status: bool, message: str) - checks if the given answer is right and
        changes reward and current points.
        self.add_player(player: Player) - adds a new player to the team
    """

    def __init__(self, team_name: str, *players):
        self.team_name = team_name
        self.active_tour = None
        self.players = list(players)
        self.problem_number = 0
        self.cur_reward = 3
        self.total_points = 0
        self.given_answers = []

    def __str__(self):
        return f'{self.team_name}'

    def start_game(self, game):
        if self.active_tour is not None:
            return False, "Нельзя участвовать в двух играх одновременно"
        self.active_tour = game
        self.problem_number = 0
        return True, f"Теперь команда {self} участвует в игре {game.name}"

    def sent_tasks(self):
        if len(self.given_answers) == 0:
            return "Вы ещё не дали ни одного ответа\n"
        res = ""
        for i in range(len(self.given_answers)):
            res += f'{i + 1}) {self.given_answers[i]}\n'
        return res

    def get_points(self):
        return True, self.total_points

    def solve(self, ans):
        if self.problem_number >= len(self.active_tour.answers):
            return False, "Вы уже дали ответ на все задачи"

        self.given_answers.append(ans)
        if ans == self.active_tour.answers[self.problem_number]:
            self.total_points += self.cur_reward
            self.cur_reward += 3
            self.problem_number += 1
            if self.problem_number >= len(self.active_tour.answers):
                return True, f"Ответ верный! Ваш текущий рейтинг: {self.total_points}, " \
                         f"это была последняя задача. Спасибо за участие!"
            return True, f"Ответ верный! Ваш текущий рейтинг: {self.total_points}, " \
                         f"награда за следующую задачу ({self.problem_number + 1} задача): {self.cur_reward}"
        else:
            self.cur_reward = max(self.cur_reward - 3, 3)
            self.problem_number += 1
            if self.problem_number >= len(self.active_tour.answers):
                return True, f"Ответ неверный! Ваш текущий рейтинг: {self.total_points}, " \
                         f"это была последняя задача. Спасибо за участие!"
            return True, f"Ответ неверный! Ваш текущий рейтинг: {self.total_points}, " \
                         f"награда за следующую задачу ({self.problem_number + 1} задача): {self.cur_reward}"

    def add_player(self, player):
        self.players.append(player)
