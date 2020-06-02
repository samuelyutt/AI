import random
from board import Board


class Agent():
    def __init__(self, side = 0):
        self.side = side


class RandomAgent(Agent):
    def __init__(self, side = 0):
        super(RandomAgent, self).__init__(side)

    def __str__(self):
        return 'Random agent'

    def take_action(self, b, movable):
        action = None
        if len(movable):
            action = random.choice(movable)
        return action

class Human(Agent):
    def __init__(self, side = 0):
        super(Human, self).__init__(side)

    def __str__(self):
        return 'Human'

    def take_action(self, b, movable):
        action = None
        if len(movable):
            while True:
                decision = input('Enter a position: ').split()
                action = (int(decision[0]), int(decision[1]))
                if action in movable:
                    break
                print('Not an available move')
        return action

        