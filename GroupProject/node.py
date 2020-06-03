import copy, math
from board import Board
from agent import RandomAgent


class Node():
    def __init__(self, board, side, tmp_side, action, parent):
        self.board = board
        self.untried_actions = self.board.movable(side)
        self.side = side
        self.tmp_side = tmp_side
        self.previous_action = action
        self.parent = parent
        self.children = []
        self.Q = 0
        self.N = 0

    def __str__(self):
        ret = '==== Node ===='
        ret += '\nQ: ' + str(self.Q)
        ret += '\nN: ' + str(self.N)
        ret += '\nside: ' + str(self.side)
        ret += '\ntmp_side: ' + str(self.tmp_side)
        ret += '\nprntprev_action: ' + (str(self.parent.previous_action) if not self.is_root() else str(None))
        ret += '\nprevious_action: ' + str(self.previous_action)
        ret += '\nchild: ' + str(len(self.children))
        ret += '\nuntried: ' + str(len(self.untried_actions))
        ret += '\nucb: ' + (str(self.UCB_value()) if not self.is_root() else str(None))
        return ret

    def is_root(self):
        return self.parent == None

    def is_leaf(self):
        return len(self.children) == 0

    def UCB_value(self, C = 1.4):
        return self.Q / self.N + C * math.sqrt(2 * math.log(self.parent.N) / self.N) if self.N else 0.0

    def select(self, C = 1.4):
        max_UCB_value = None
        select_c = None
        for c in self.children:
            UCB_value = c.UCB_value(C)
            if max_UCB_value == None or UCB_value > max_UCB_value:
                max_UCB_value = UCB_value
                select_c = c
        return select_c

    def expand(self):
        action = self.untried_actions.pop()
        next_board = copy.deepcopy(self.board)
        next_board.move(self.tmp_side, action)
        child = Node(next_board, self.side, self.tmp_side * -1, action, self)
        self.children.append(child)
        return child

    def update(self, winner_side):
        self.N += 1
        if winner_side == self.side:
            self.Q += 1
        elif winner_side == self.side * -1:
            self.Q -= 1
        if not self.is_root():
            self.parent.update(winner_side)

    def rollout(self):
        tmp_board = copy.deepcopy(self.board)
        side = self.tmp_side
        agent = RandomAgent(side)
        stuck_count = 0
        while True:
            movable = tmp_board.movable(side)
            if len(movable):
                action = agent.take_action(tmp_board, movable)
                tmp_board.move(side, action)
                stuck_count = 0
            else:
                stuck_count += 1
            if stuck_count == 2:
                black_count, white_count = tmp_board.statistics()
                result = black_count - white_count
                if result > 0:
                    return 1
                elif result < 0:
                    return -1
                elif result == 0:
                    return 0
                break
            side *= -1

