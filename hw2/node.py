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

    def board_status(self, b):
        status = []
        for i in range(b.size_x * b.size_y):
            status.append(9)
        for variable in self.asgn_vrbls:
            status[variable.position[1] * b.size_x + variable.position[0]] = variable.assignment
        ret = ''
        for s in status:
            ret += str(s)
        return ret

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

    def forward_checking(self, b, position):
        fc_err = 0
        is_mine_pos = []
        no_mine_pos = []
        check_pos = b.around_position(position)
        for pos in check_pos:
            hint = b.hints[pos[0]][pos[1]]
            if hint > -1:
                lower_bound, upper_bound = b.forward_checking_limit(self.asgn_vrbls, pos)
                if lower_bound > hint or upper_bound < hint:
                    fc_err = -1
                    break
                elif lower_bound == hint:
                    no_mine_pos += b.around_position(pos)
                elif upper_bound == hint:
                    is_mine_pos += b.around_position(pos)
        if not fc_err:
            for variable in self.unas_vrbls:
                pos = variable.position
                if (pos[0], pos[1]) in no_mine_pos:
                    try:
                        variable.domain.remove(1)
                    except:
                        pass
                if (pos[0], pos[1]) in is_mine_pos:
                    try:
                        variable.domain.remove(0)
                    except:
                        pass                    
                if len(variable.domain) == 0:
                    fc_err = -1
                    break
        return fc_err

    def mrv(self, sort_bound):
        sort_count = 0
        groups = [[], []]
        for i in range(len(self.unas_vrbls) - sort_bound, len(self.unas_vrbls)):
            variable = self.unas_vrbls[i]
            if len(variable.domain) == 1:
                groups[0].append(variable)
                sort_count += 1
            else:
                groups[1].append(variable)
        self.unas_vrbls = groups[1] + groups[0]
        sort_count = sort_bound if sort_count == 0 else sort_count
        return sort_count

    def dh(self, sort_bound, b):
        groups = [[], [], [], [], [], [], [], [], []]
        current = b.current_board(self.asgn_vrbls)
        for i in range(len(self.unas_vrbls) - sort_bound, len(self.unas_vrbls)):
            variable = self.unas_vrbls[i]
            around = b.around_position(variable.position)
            degree = 0
            for a in around:
                if current[a[0]][a[1]] == -1:
                    degree += 1
            groups[degree].append(variable)

        sort_vrbls = []
        for group in groups[::-1]:
            sort_vrbls += group
        self.unas_vrbls = self.unas_vrbls[0:len(self.unas_vrbls) - sort_bound] + sort_vrbls
        return sort_bound


if __name__ == '__main__':
    inputs = '6 6 10 -1 -1 -1 1 1 -1 -1 3 -1 -1 -1 0 2 3 -1 3 3 2 -1 -1 2 -1 -1 -1 -1 2 2 3 -1 3 -1 1 -1 -1 -1 1'
    b = Board(inputs)
    
    variables = []
    for j in range(b.size_y):
        for i in range(b.size_x):
            if b.hints[i][j] == -1:
                variables.append(Variable(i, j))