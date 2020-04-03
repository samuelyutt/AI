from board import position


class node:
    def __init__(self, parent_, position_, depth_ = -1):
        self.parent = parent_
        self.position = position_
        self.childs = []
        self.depth = depth_

    def __str__(self):
        return self.position.__str__()

    def __repr__(self):
        return self.position.__str__()

    def __lt__(self, other):
        return self.position < other.position

    def add_child(self, child_node):
        self.childs.append(child_node)