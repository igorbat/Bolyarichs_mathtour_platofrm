from karusel.karusel_game import GameKarusel
from karusel.player import Player
from karusel.team import Team


class StateMachine:
    """
    Class describing current condition of the players, teams and games
    #TODO doesn't support multiple tours at the same time

    Attributes:
        self.players - a dict of all players. Key is the unique id of the player,
        value is the object of class Player
        self.tours - a dict of all tours. Key is the name of the tour,
        value is the object of class GameKarusel
        self.teams - a dict of all teams. Key is the name of the team,
        value is the object of class Team
        self.cnt_of_the_team_name - a dict that helps to understand how many people has the same team name

    Methods:
        self.add_tour(tour_name: str, game: GameKarusel) - adds a particular tour
        self.register_player(player_id: str, team_name: str) -> name_of_the_team: str -
        - registers player to a partcilar team
        self.join_tour(player_id: str, tour_name: str) -> (status: bool, message: str) -
        registers a team to the particular tour
        self.solve(player_id: str, *parts) -> (status: bool, message: str) - allows a person to
        send answers to the tasks. parts is the consistence of the answer
        self.tasks(player_id: str) -> (status: bool, message: str) - returns tasks to the particular tour
        self.sent_tasks(player_id: str) -> (status: bool, message: str) - returns a string describing given answers
        self.points(player_id: str) -> (status: bool, message: str) - return current points of the player
        self.get_sorted_res() -> str - returns a string describing current condition (number of points) for each team
    """

    def __init__(self):
        self.players: dict[str, Player] = {}
        self.tours: dict[str, GameKarusel] = {}
        self.teams: dict[str, Team] = {}
        self.cnt_of_the_team_name: dict[str, int] = {}

    def add_tour(self, tour_name, game):
        self.tours[tour_name] = game

    def register_player(self, player_id, team_name):
        if player_id in self.players:
            return f"У вас уже есть команда: {str(self.players[player_id].team)}"

        player = Player(player_id)

        if team_name not in self.cnt_of_the_team_name:
            self.cnt_of_the_team_name[team_name] = 1
            team_name += f'-{self.cnt_of_the_team_name[team_name]}'
            self.teams[team_name] = Team(team_name, player)
        else:
            self.cnt_of_the_team_name[team_name] += 1
            team_name += f'-{self.cnt_of_the_team_name[team_name]}'
            self.teams[team_name] = Team(team_name, player)

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

        if self.players[player_id].team.active_tour is None:
            return False, "Игрок не участвует ни в одном соревновании"

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
        if len(self.teams.values()) == 0:
            return "Нет ни одной команды"
        res = sorted(self.teams.values(), key=lambda x: -x.total_points)
        ans = ""

        for el in res:
            ans += f'{el.team_name} - {el.total_points}\n'
        return ans

    def reload_res(self):
        pass
