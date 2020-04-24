import copy
from variable import Assigned_Variable
from variable import Unassigned_Variable
from board import Board
from node import Node


class Agent():
    def __init__(self, fc = True, mrv = False, dh = False, lcv = False):
        self.fc = fc
        self.mrv = mrv
        self.dh = dh
        self.lcv = lcv

    def search(self, b):
        unas_vrbls = []
        for j in range(b.size_y):
            for i in range(b.size_x):
                if b.hints[i][j] == -1:
                    unas_vrbls.append(Unassigned_Variable((i, j)))
        
        root = Node([], copy.deepcopy(unas_vrbls), None)

        explorered_set = []
        frontier = [root]

        while len(frontier):
            # Expand the deepest (most recent) unexpanded node
            cur_node = frontier.pop()

            current = cur_node.board_status(b)
            if current in explorered_set:
                continue
            explorered_set.append(current)

            # Return when solution is found
            cc = cur_node.consistency_check(b)
            if cc < 0:
                continue
            elif cc == 0 and len(cur_node.unas_vrbls) == 0:
                return cur_node
            elif len(cur_node.unas_vrbls) == 0:
                continue

            # Forward checking (Optional)
            if self.fc:
                if cur_node.last_sltd_vrbl is not None:
                    if cur_node.forward_checking(b, cur_node.last_sltd_vrbl.position) != 0:
                        continue
            
            # Choose a variable to expand
            sort_count = len(cur_node.unas_vrbls)
            if self.mrv:
                # for variable in cur_node.unas_vrbls:
                #     print(len(variable.domain), end=" ")
                # print(sort_count)
                sort_count = cur_node.mrv(sort_count)
                # for variable in cur_node.unas_vrbls:
                #     print(len(variable.domain), end=" ")
                # print(sort_count)
                # print()
            if self.dh:
                sort_count = cur_node.dh(sort_count, b)
            if self.lcv:
                cur_node.lcv(sort_count)
            
                
            sltd_vrbl = cur_node.unas_vrbls.pop()

            for value in sltd_vrbl.domain:
                child_asgn_vrbls = copy.deepcopy(cur_node.asgn_vrbls)
                child_asgn_vrbls.append(Assigned_Variable(sltd_vrbl.position, value))
                child_unas_vrbls = copy.deepcopy(cur_node.unas_vrbls)
                child = Node(child_asgn_vrbls, child_unas_vrbls, sltd_vrbl)
                cur_node.add_child(child)
                frontier.append(child)
        
        return None


if __name__ == '__main__':
    inputs_list = ['6 6 10 -1 -1 -1 1 1 -1 -1 3 -1 -1 -1 0 2 3 -1 3 3 2 -1 -1 2 -1 -1 -1 -1 2 2 3 -1 3 -1 1 -1 -1 -1 1',
                   '6 6 10 -1 -1 -1 1 1 1 3 4 -1 2 -1 -1 2 -1 -1 -1 -1 -1 -1 -1 2 2 -1 2 1 2 -1 -1 1 -1 -1 1 -1 1 0 -1',
                   '6 6 10 -1 -1 -1 -1 -1 -1 -1 2 2 2 3 -1 -1 2 0 0 2 -1 -1 2 0 0 2 -1 -1 3 2 2 2 -1 -1 -1 -1 -1 -1 -1', 
                   '6 6 10 -1 1 -1 1 1 -1 2 2 3 -1 -1 1 -1 -1 5 -1 5 -1 2 -1 5 -1 -1 -1 -1 2 -1 -1 3 -1 -1 -1 1 1 -1 0']
    
    # inputs_list = ['6 6 10 -1 -1 -1 1 1 -1 -1 3 -1 -1 -1 0 2 3 -1 3 3 2 -1 -1 2 -1 -1 -1 -1 2 2 3 -1 3 -1 1 -1 -1 -1 1']
    # inputs_list = ['6 6 10 -1 -1 -1 -1 -1 -1 -1 2 2 2 3 -1 -1 2 0 0 2 -1 -1 2 0 0 2 -1 -1 3 2 2 2 -1 -1 -1 -1 -1 -1 -1']
    
    a = Agent(mrv = True, dh = True)
    for inputs in inputs_list:
        b = Board(inputs)
        result = a.search(b)
        if result != None:
            b.print_board(result.asgn_vrbls)
        print()

        