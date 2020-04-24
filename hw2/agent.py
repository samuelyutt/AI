import copy
from variable import Assigned_Variable
from variable import Unassigned_Variable
from board import Board
from node import Node


class Agent():
    def __init__(self):
        pass

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

            # current = cur_node.board_status(b)
            # print(current)
            # for explorered in explorered_set:
            #     if current == explorered:
            #         print(564161)
            #         break
            # if current in explorered_set:
            #     print(current)
            #     continue
            # else:
            #     explorered_set.append(current)

            # Return when solution is found
            cc = cur_node.consistency_check(b)
            if cc < 0:
                continue
            elif cc == 0 and len(cur_node.unas_vrbls) == 0:
                return cur_node
            elif len(cur_node.unas_vrbls) == 0:
                continue
            
            # Choose a variable to expand
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
    for inputs in inputs_list:
        b = Board(inputs)
        a = Agent()
        result = a.search(b)
        b.print_board(result.asgn_vrbls)
        print()

        