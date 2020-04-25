import copy
from variable import Variable
from variable import Assigned_Variable
from variable import Unassigned_Variable
from board import Board


class Node():
    def __init__(self, asgn_vrbls, unas_vrbls, last_sltd_vrbl):
        self.asgn_vrbls = asgn_vrbls
        self.unas_vrbls = unas_vrbls
        self.last_sltd_vrbl = last_sltd_vrbl
        self.childs = []

    def add_child(self, child_node):
        self.childs.append(child_node)

    def board_status_string(self, b):
        # Return the string of board status of this node
        # Used for explored set
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
        # Check all arc arc-consistent
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
            return -1, -1

        # Check all arc arc-consistent
        all_acc_count = self.all_arc_consistent_check(b)
        if all_acc_count < 0:
            return -1, -2

        return gcc_count, all_acc_count

    def forward_checking(self, b, position):
        fc_err = 0
        is_mine_pos = []
        no_mine_pos = []
        check_pos = b.around_position(position)

        # Find positions that can only be mine and positions that can not be mine
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
        
        # Remove values from the domain of varaibles whose position is in positions found above
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

        # Categorize by remaining values
        groups = [[], []]
        for i in range(len(self.unas_vrbls) - sort_bound, len(self.unas_vrbls)):
            variable = self.unas_vrbls[i]
            if len(variable.domain) == 1:
                groups[0].append(variable)
                sort_count += 1
            else:
                groups[1].append(variable)
        
        # Sort by reverse order
        self.unas_vrbls = groups[1] + groups[0]
        sort_count = sort_bound if sort_count == 0 else sort_count
        return sort_count

    def degree_hrs(self, b, last_sltd_vrbl, sort_bound):
        sort_count = sort_bound
        if last_sltd_vrbl is not None:
            # Categorize by degree
            groups = [[], [], [], [], [], [], [], [], []]
            for i in range(len(self.unas_vrbls) - sort_bound, len(self.unas_vrbls)):
                variable = self.unas_vrbls[i]                
                groups[variable.degree].append(variable)

            # Sort
            sort_vrbls = []
            for group in groups:
                sort_vrbls += group
                sort_count = len(group) if len(group) != 0 else sort_count
            self.unas_vrbls = self.unas_vrbls[0:len(self.unas_vrbls) - sort_bound] + sort_vrbls
        return sort_count

    def space_hrs(self, b, last_sltd_vrbl, sort_bound):
        sort_count = sort_bound
        if last_sltd_vrbl is not None:
            # Update space degree
            around = b.around_position(last_sltd_vrbl.position) 
            for variable in self.unas_vrbls:
                if variable.position in around:
                    variable.degree -= 1

            # Categorize by space degree
            groups = [[], [], [], [], [], [], [], [], []]
            for i in range(len(self.unas_vrbls) - sort_bound, len(self.unas_vrbls)):
                variable = self.unas_vrbls[i]                
                groups[variable.degree].append(variable)

            # Sort by reverse order
            sort_vrbls = []
            for group in groups[::-1]:
                sort_vrbls += group
                sort_count = len(group) if len(group) != 0 else sort_count
            self.unas_vrbls = self.unas_vrbls[0:len(self.unas_vrbls) - sort_bound] + sort_vrbls
        return sort_count

    def lcv(self, b):
        variable = self.unas_vrbls[-1]
        
        # Only for variables whose domains are still [0 ,1]
        if len(variable.domain) == 2:
            limit_pos_counts = []
            
            # Try both values
            for value in variable.domain:
                new_asgn_vrbls = copy.deepcopy(self.asgn_vrbls)
                new_asgn_vrbls.append(Assigned_Variable(variable.position, value))
                new_unas_vrbls = copy.deepcopy(self.unas_vrbls)
                new_board = b.current_board(new_asgn_vrbls)

                # Foward check to calculate count of ruled out values
                fc_err = 0
                limit_pos = []
                check_pos = b.around_position(variable.position)
                for pos in check_pos:
                    hint = b.hints[pos[0]][pos[1]]
                    if hint > -1:
                        lower_bound, upper_bound = b.forward_checking_limit(new_asgn_vrbls, pos)
                        if lower_bound > hint or upper_bound < hint:
                            fc_err = -1
                            break
                        elif lower_bound == hint or upper_bound == hint:
                            around = b.around_position(pos)
                            for a in around:
                                if a not in limit_pos and new_board[a[0]][a[1]] == -1:
                                    limit_pos.append(a)
                if fc_err != -1:
                    limit_pos_counts.append(len(limit_pos))
                else:
                    limit_pos_counts.append(-1)
            
            # Switch domain if need
            if limit_pos_counts != [-1, -1]:
                if limit_pos_counts[1] < limit_pos_counts[0]:
                    variable.domain = [1, 0]
            
            # Remove value from domain if need
            if limit_pos_counts[1] == -1:
                try:
                    variable.domain.remove(1)
                except:
                    pass
            if limit_pos_counts[0] == -1:
                try:
                    variable.domain.remove(0)
                except:
                    pass


if __name__ == '__main__':
    # Some expamples
    inputs = '6 6 10 -1 -1 -1 1 1 -1 -1 3 -1 -1 -1 0 2 3 -1 3 3 2 -1 -1 2 -1 -1 -1 -1 2 2 3 -1 3 -1 1 -1 -1 -1 1'
    b = Board(inputs)
    
    variables = []
    for j in range(b.size_y):
        for i in range(b.size_x):
            if b.hints[i][j] == -1:
                variables.append(Variable(i, j))

