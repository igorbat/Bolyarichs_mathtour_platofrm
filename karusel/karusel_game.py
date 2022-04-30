class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.team: Team = None

    def set_team(self, team):
        self.team = team


class GameKarusel:
    def __init__(self, name, link, answers):
        self.name = name
        self.link = link
        self.tasks_amount = len(answers)
        self.answers = answers

    def get_name(self):
        return self.name

    def get_tasks(self):
        return self.link


class Team:
    def __init__(self, team_name: str, *players):
        self.team_name = team_name
        self.active_tour = None
        self.players = list(players)
        self.problem_number = 0
        self.cur_reward = 3
        self.total_points = 0
        self.given_answers = []

    def __str__(self):
        return f'{self.team_name}-{len(self.players)}'

    def start_game(self, game: GameKarusel):
        if self.active_tour is not None:
            return False, "Нельзя учавствовать в двух играх одновременно"
        self.active_tour = game
        self.problem_number = 0
        return True, f"Теперь команда {self} учавствует в игре {game.name}"

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

    def add_player(self, player: Player):
        self.players.append(player)


class StateMachine:
    def __init__(self):
        self.players: dict[str, Player] = {}
        self.tours: dict[str, GameKarusel] = {}
        self.teams: dict[str, Team] = {}

    def add_tour(self, tour_name, game):
        self.tours[tour_name] = game

    def register_player(self, player_id, team_name):
        if player_id in self.players:
            return f"У вас уже есть команда: {str(self.players[player_id].team)}"

        player = Player(player_id)

        if team_name not in self.teams:
            self.teams[team_name] = Team(team_name, player)
        else:
            self.teams[team_name].add_player(player)

        player.set_team(self.teams[team_name])
        self.players[player_id] = player

        return str(player.team)

    def join_tour(self, player_id, tour_name):
        if tour_name not in self.tours:
            return False, "Нет такого турнира"

        if player_id not in self.players:
            return False, "Нет такого игрока"

        is_ok, msg = self.players[player_id].team.start_game(self.tours[tour_name])
        return is_ok, msg

    def solve(self, player_id, *parts):
        if player_id not in self.players:
            return False, "Нет такого игрока"

        if len(parts) != 1:
            return False, "Неверный формат ответа. Ответ должен иметь такой вид: '!solve ANSWER'"

        is_ok, msg = self.players[player_id].team.solve(parts[0])
        return is_ok, msg

    def tasks(self, player_id):
        if player_id not in self.players:
            return False, "Нет такого игрока"
        if self.players[player_id].team.active_tour is None:
            return False, "Вы нигде не играете"
        return True, self.players[player_id].team.active_tour.get_tasks()

    def sent_task(self, player_id):
        if player_id not in self.players:
            return False, "Нет такого игрока"
        if self.players[player_id].team.active_tour is None:
            return False, "Вы нигде не играете"
        return True, self.players[player_id].team.sent_tasks()

    def points(self, player_id):
        if player_id not in self.players:
            return False, "Нет такого игрока"
        is_ok, msg = self.players[player_id].team.get_points()
        return is_ok, msg

    def get_sorted_res(self):
        pass

    def reload_res(self):
        pass
