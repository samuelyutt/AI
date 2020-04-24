from variable import Variable
from board import Board


class Node():
    def __init__(self, asgn_vrbls, unas_vrbls, last_sltd_vrbl):
        self.asgn_vrbls = asgn_vrbls
        self.unas_vrbls = unas_vrbls
        self.last_sltd_vrbl = last_sltd_vrbl
        self.childs = []

    def add_child(self, child_node):
        self.childs.append(child_node)

    def all_arc_consistent_check(self, b):
        acc_count = 0
        for j in range(b.size_y):
            for i in range(b.size_x):
                position = (i, j)
                acc = b.arc_consistent_check(self.asgn_vrbls, position)
                if acc < 0:
                    return -1
                acc_count += acc
        return acc_count

    def consistency_check(self, b):
        # Check global constraint
        gcc_count = b.global_constraint_check(self.asgn_vrbls)
        if gcc_count < 0:
            return -1

        # Check all arc arc-consistent
        all_acc_count = self.all_arc_consistent_check(b)
        if all_acc_count < 0:
            return -2

        return gcc_count + all_acc_count

    def is_solution(self, b):
        if len(self.unas_vrbls) == 0:
            return False
        if self.consistency_check(b) == 0:
            return True
        else:
            return False


if __name__ == '__main__':
    inputs = '6 6 10 -1 -1 -1 1 1 -1 -1 3 -1 -1 -1 0 2 3 -1 3 3 2 -1 -1 2 -1 -1 -1 -1 2 2 3 -1 3 -1 1 -1 -1 -1 1'
    b = Board(inputs)
    
    variables = []
    for j in range(b.size_y):
        for i in range(b.size_x):
            if b.hints[i][j] == -1:
                variables.append(Variable(i, j))