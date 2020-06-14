import copy, time
from node import Node
from agent import Agent
from board import Board


class MCTSAgent(Agent):
    def __init__(self, iteration_count = 200, side = 0, type_ = 2):
        super(MCTSAgent, self).__init__(side)
        self.iteration_count = iteration_count
        self.type = type_

    def __str__(self):
        return 'MCTS agent (' + str(self.iteration_count) + ')'

    def iteration(self, root):
        start = time.time()
        # for _ in range(self.iteration_count):
        while time.time() - start < 4.6:
            rollout_node = self.selection2(root) if self.type == 2 else self.selection(root)
            result = self.simulation(rollout_node)
            self.backpropagation(rollout_node, result)
        return root.select(0.0)

    def selection(self, root):
        current_node = root
        if len(current_node.untried_actions):
            current_node = self.expansion(current_node)
        else:
            while not current_node.is_leaf():
                current_node = current_node.select()
        return current_node
        
    def selection2(self, root):
        current_node = root
        while True:
            if len(current_node.untried_actions):
                current_node = self.expansion(current_node)
                break
            if current_node.is_leaf():
                break
            current_node = current_node.select()
        return current_node

    def expansion(self, node):
        new_node = node.expand()
        return new_node

    def simulation(self, node):
        result = node.rollout()
        return result

    def backpropagation(self, node, result):
        node.update(result)

    def take_action(self, b, movable):
        action = None
        if len(movable):
            root = Node(copy.deepcopy(b), self.side, self.side, None, None)
            select_node = self.iteration(root)
            action = select_node.previous_action
            # for c in root.children:
            #     print(c)
            #     print(c.UCB_value(0.0))
            # if not select_node.is_leaf():
            #     print('cc')
            #     for cc in select_node.children:
            #         print(cc)
        return action

