class Player:
    """
    Class representing usual player
    Attributes:
        self.player_id - unique id of the player
        self.team - team which the player joins

    Methods:
        self.set_team(team: Team) - sets the team of the player
    """

    def __init__(self, player_id):
        self.player_id = player_id
        self.team = None

    def set_team(self, team):
        self.team = team