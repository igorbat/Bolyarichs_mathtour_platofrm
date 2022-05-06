class GameKarusel:
    """
    Class representing game
    Attributes:
        self.name - name of the game
        self.link - link to the tasks
        self.tasks_amount - amount of tasks
        self.answer - answers to the tasks

    Methods:
        self.get_name() -> str - returns the name of the game
        self.get_tasks() -> str - returns link to the tasks
    """

    def __init__(self, name, link, answers):
        self.name = name
        self.link = link
        self.tasks_amount = len(answers)
        self.answers = answers

    def get_name(self):
        return self.name

    def get_tasks(self):
        return self.link
