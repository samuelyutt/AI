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


class DullAgent(Agent):
    def __init__(self, side = 0):
        super(DullAgent, self).__init__(side)

    def __str__(self):
        return 'Dull agent'

    def take_action(self, b, movable):
        action = None
        flip_pos_count = -1
        if len(movable):
            action = movable[-1]
        return action


class GreedyAgent(Agent):
    def __init__(self, side = 0):
        super(GreedyAgent, self).__init__(side)

    def __str__(self):
        return 'Greedy agent'

    def take_action(self, b, movable):
        action = None
        flip_pos_count = -1
        if len(movable):
            for a in movable:
                tmp = len(b.flip_positions(self.side, a))
                if tmp > flip_pos_count:
                    action = a
                    flip_pos_count = tmp
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
                if len(decision) == 2:
                    action = (int(decision[0]), int(decision[1]))
                    if action in movable:
                        break
                print('Not an available move')
        return action

        