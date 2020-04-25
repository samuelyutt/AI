import time, copy
from variable import Assigned_Variable
from variable import Unassigned_Variable
from board import Board
from node import Node


class Agent():
    def __init__(self, fc = True, mrv = False, heuristic = '', lcv = False):
        self.fc = fc
        self.mrv = mrv
        self.heuristic = heuristic
        self.lcv = lcv

    def search(self, b):
        # Initial unassigned variables
        unas_vrbls = []
        for j in range(b.size_y):
            for i in range(b.size_x):
                if b.hints[i][j] == -1:
                    variable = Unassigned_Variable((i, j), b, self.heuristic)
                    unas_vrbls.append(variable)
        
        # Create the root node
        root = Node([], copy.deepcopy(unas_vrbls), None)

        # Initial explored set and frontier
        # Frontier: stack
        explorered_set = []
        frontier = [root]

        while len(frontier):
            # Expand the deepest (most recent) unexpanded node
            cur_node = frontier.pop()

            # Check and set explorered set
            current = cur_node.board_status_string(b)
            if current in explorered_set:
                continue
            explorered_set.append(current)

            # Return the node when solution is found
            # or skip this node if not consistent
            gcc, all_acc = cur_node.consistency_check(b)
            cc = gcc + all_acc
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
            
            # Heuristics (Optional)
            sort_count = len(cur_node.unas_vrbls)            
            # MRV
            if self.mrv:
                sort_count = cur_node.mrv(sort_count)
            # Degree heuristic or Space heuristic
            if self.heuristic == 'degree':
                sort_count = cur_node.degree_hrs(b, cur_node.last_sltd_vrbl, sort_count)
            elif self.heuristic == 'space':                
                sort_count = cur_node.space_hrs(b, cur_node.last_sltd_vrbl, sort_count)
            # LCV
            if self.lcv:
                cur_node.lcv(b)

            # Choose the selected variable to expand
            sltd_vrbl = cur_node.unas_vrbls.pop()

            for value in sltd_vrbl.domain:
                # Create child node and append to parent
                child_asgn_vrbls = copy.deepcopy(cur_node.asgn_vrbls)
                child_asgn_vrbls.append(Assigned_Variable(sltd_vrbl.position, value))
                child_unas_vrbls = copy.deepcopy(cur_node.unas_vrbls)
                child = Node(child_asgn_vrbls, child_unas_vrbls, sltd_vrbl)
                cur_node.add_child(child)
                
                # Set frontier
                frontier.append(child)
        
        # Return None if no solution is found
        return None


if __name__ == '__main__':
    # Some examples and tests
    inputs_list = ['6 6 10 -1 -1 -1 1 1 -1 -1 3 -1 -1 -1 0 2 3 -1 3 3 2 -1 -1 2 -1 -1 -1 -1 2 2 3 -1 3 -1 1 -1 -1 -1 1',
                   '6 6 10 -1 -1 -1 1 1 1 3 4 -1 2 -1 -1 2 -1 -1 -1 -1 -1 -1 -1 2 2 -1 2 1 2 -1 -1 1 -1 -1 1 -1 1 0 -1',
                   '6 6 10 -1 -1 -1 -1 -1 -1 -1 2 2 2 3 -1 -1 2 0 0 2 -1 -1 2 0 0 2 -1 -1 3 2 2 2 -1 -1 -1 -1 -1 -1 -1', 
                   '6 6 10 -1 1 -1 1 1 -1 2 2 3 -1 -1 1 -1 -1 5 -1 5 -1 2 -1 5 -1 -1 -1 -1 2 -1 -1 3 -1 -1 -1 1 1 -1 0']
    
    start_time = time.time()

    a = Agent(fc = True, mrv = True, heuristic = 'space', lcv = False)
    for inputs in inputs_list:
        b = Board(inputs)
        result = a.search(b)
        if result != None:
            b.print_board(result.asgn_vrbls)
        print()

    search_time = (time.time() - start_time) * 100
    print(search_time)

        