import copy
from node import Node
from agent import Agent
from board import Board


class MCTSAgent(Agent):
    def __init__(self, iteration_count = 200, side = 0):
        super(MCTSAgent, self).__init__(side)
        self.iteration_count = iteration_count

    def __str__(self):
        return 'MCTS agent (' + str(self.iteration_count) + ')'

    def iteration(self, root):
        for _ in range(self.iteration_count):
            rollout_node = self.selection(root)
            result = self.simulation(rollout_node)
            self.backprpogation(rollout_node, result)
        return root.select(0.0)

    def selection(self, root):
        current_node = root
        if len(current_node.untried_actions):
            current_node = self.expansion(current_node)
        else:
            while not current_node.is_leaf():
                current_node = current_node.select()
        return current_node

    def expansion(self, node):
        new_node = node.expand()
        return new_node

    def simulation(self, node):
        result = node.rollout()
        return result

    def backprpogation(self, node, result):
        node.update(result)

    def take_action(self, b, movable):
        action = None
        if len(movable):
            root = Node(copy.deepcopy(b), self.side, self.side, None, None)
            select_node = self.iteration(root)
            action = select_node.previous_action
        return action

