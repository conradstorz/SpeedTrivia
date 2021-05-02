"""
Team object?
Team
    members
    current round
        used points
        current question
"""
import datetime

class Team():

    # Class-level variables
    instances = {}

    def __init__(self, name):
        self.name = name
        self.round = 1
        self.question = 1
        self.spent_points = []
        self.__class__.instances[self.name] = self

    def submit_answer(self, points):
        if points in self.spent_points:
            return False

        valid = False
        if self.round in (1,2,3) and points in (2,4,6):
            valid = True
        elif self.round in (4,5,6) and points in (5,7,9):
            valid = True
        elif self.round == 'halftime':
            valid = True
        elif self.round == 'final' and points >= 0 and points <= 20:
            valid = True
        elif self.round == 'tiebreaker':
            raise NotImplementedError("Don't know what points are valid for tiebreaker. None?")
        
        if valid:
            self.spent_points.append(points)
            self.increment_question()
            return True
        else:
            return False

    def increment_question(self):
        # increment rounds
        if self.round in ('halftime', 'final') or self.question == 3:
            self.increment_round()
        else:
            self.question += 1

    def increment_round(self):
        self.question = 1
        self.spent_points = []

        if self.round == 3:
            self.round = 'halftime'
        elif self.round == 'halftime':
            self.round = 4
        elif self.round == 6:
            self.round = 'final'
        elif self.round == 'final':
            self.round = 'tiebreaker'
        elif self.round == 'tiebreaker':
            raise ValueError("Tiebreaker is the final round!")
        else:
            self.round += 1

    @classmethod
    def get_team_by_name(cls, name):
        return cls.instances.get(name, None)