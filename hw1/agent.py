import math
import queue
import bisect
from board import board
from board import position
from tree import node

def heuristic(pos, goal):
    # This function returns the value of heuristic function
    return int( (abs(pos.x-goal.x) + abs(pos.y-goal.y)) / 3 )

def estimated_cost(g, node, goal):
    # This function returns the value of estimated cost
    return g + heuristic(node.position, goal)

def path_list(goal_node):
    # This function returns a list of positions of the
    # path moving from starting position to goal position
    # by order 
    ret = []
    tmp_node = goal_node
    while tmp_node != None:
        ret.append(tmp_node.position)
        tmp_node = tmp_node.parent
    ret.reverse()
    return ret


class agent:
    def __init__(self, start_, goal_):
        self.expanded_node_count = 0
        self.start = start_
        self.goal = goal_

    def add_expanded_node(self):
        self.expanded_node_count += 1


class bfs(agent):
    def __init__(self, start_, goal_):
        super(bfs, self).__init__(start_, goal_)

    def __str__(self):
        return "BFS"

    def __repr__(self):
        return self.__str__()

    def search(self, b):
        # Create the root node
        root = node(None, self.start)

        # Initial explored set and frontier
        # Frontier: queue
        explorered_set = []
        frontier = queue.Queue(maxsize = -1)
        frontier.put(root)
        
        while not frontier.empty():
            # Expand shallowest unexpanded node
            cur_node = frontier.get()
            
            # Return when path is found
            if cur_node.position == self.goal:
                return path_list(cur_node)
            if cur_node.position in explorered_set:
                continue

            possible_moves = cur_node.position.available_moves(b)
            self.add_expanded_node()
            explorered_set.append(cur_node.position)

            for new_pos in possible_moves:
                # Create child node and append to parent
                child = node(cur_node, new_pos)
                cur_node.add_child(child)
                
                # Set frontier
                frontier.put(child)
        return []


class dfs(agent):
    def __init__(self, start_, goal_):
        super(dfs, self).__init__(start_, goal_)

    def __str__(self):
        return "DFS"

    def __repr__(self):
        return self.__str__()

    def search(self, b):
        # Create the root node
        root = node(None, self.start)

        # Initial explored set and frontier
        # Frontier: stack
        explorered_set = []
        frontier = [root]
        
        while len(frontier):
            # Expand the deepest (most recent) unexpanded node
            cur_node = frontier.pop()

            # Return when path is found
            if cur_node.position == self.goal:
                return path_list(cur_node)
            if cur_node.position in explorered_set:
                continue
            
            possible_moves = cur_node.position.available_moves(b)
            self.add_expanded_node()
            explorered_set.append(cur_node.position)

            for new_pos in possible_moves:
                # Create child node and append to parent
                child = node(cur_node, new_pos)
                cur_node.add_child(child)
                
                # Set frontier
                frontier.append(child)
        return []


class ids(agent):
    def __init__(self, start_, goal_):
        super(ids, self).__init__(start_, goal_)

    def __str__(self):
        return "IDS"

    def __repr__(self):
        return self.__str__()

    def search(self, b):
        # Initial depth limit
        depth_limit = -1

        while True:
            # Set depth limit
            depth_limit += 1

            # Create the root node
            root = node(None, self.start, 0)

            # Initial explored set and frontier
            # Frontier: stack
            explorered_set = []
            frontier = [root]
            
            while len(frontier):
                # Expand the deepest (most recent) unexpanded node
                # where depth not greater than depth limit
                cur_node = frontier.pop()
                
                # Return when path is found
                if cur_node.position == self.goal:
                    return path_list(cur_node)
                if cur_node.depth == depth_limit:
                    continue
                if cur_node.position in explorered_set:
                    continue
                
                possible_moves = cur_node.position.available_moves(b)
                self.add_expanded_node()
                explorered_set.append(cur_node.position)

                for new_pos in possible_moves:
                    # Create child node and append to parent
                    child = node(cur_node, new_pos, cur_node.depth+1)
                    cur_node.add_child(child)
                    
                    # Set frontier
                    frontier.append(child)
                    
                    if len(explorered_set) >= math.pow(b.size, 2):
                        return []
        return []


class astar(agent):
    def __init__(self, start_, goal_):
        super(astar, self).__init__(start_, goal_)

    def __str__(self):
        return "A*"

    def __repr__(self):
        return self.__str__()

    def search(self, b):
        # Create the root node
        root = node(None, self.start, 0)
        
        # Initial explored set and frontier
        # Frontier: priority queue
        explorered_set = []
        frontier = []
        pair = (estimated_cost(root.depth, root, self.goal), root)
        bisect.insort(frontier, pair)
        
        while len(frontier):
            # Expand the unexpanded node with the lowest
            # estimated total path cost
            cur_node = frontier.pop(0)[1]
            
            # Return when path is found
            if cur_node.position == self.goal:
                return path_list(cur_node)
            if cur_node.position in explorered_set:
                continue

            possible_moves = cur_node.position.available_moves(b)
            self.add_expanded_node()
            explorered_set.append(cur_node.position)

            for new_pos in possible_moves:
                # Create child node and append to parent
                child = node(cur_node, new_pos, cur_node.depth+1)
                cur_node.add_child(child)
                
                # Set frontier
                pair = (estimated_cost(child.depth, child, self.goal), child)
                bisect.insort(frontier, pair)
        return []


class idastar(agent):
    def __init__(self, start_, goal_):
        super(idastar, self).__init__(start_, goal_)

    def __str__(self):
        return "IDA*"

    def __repr__(self):
        return self.__str__()

    def search(self, b):
        # Initial depth limit
        depth_limit = -1

        while True:
            # Set depth limit
            depth_limit += 1

            # Create the root node
            root = node(None, self.start, 0)

            # Initial explored set and frontier
            # Frontier: priority queue
            explorered_set = []
            frontier = []
            pair = (estimated_cost(root.depth, root, self.goal), root)
            bisect.insort(frontier, pair)
            
            while len(frontier):   
                # Expand the unexpanded node with the lowest
                # estimated total path cost 
                # where depth not greater than depth limit
                cur_node = frontier.pop(0)[1]
                
                # Return when path is found
                if cur_node.position == self.goal:
                    return path_list(cur_node)
                if cur_node.depth == depth_limit:
                    continue
                if cur_node.position in explorered_set:
                    continue
                
                possible_moves = cur_node.position.available_moves(b)
                self.add_expanded_node()
                explorered_set.append(cur_node.position)

                for new_pos in possible_moves:
                    # Create child node and append to parent
                    child = node(cur_node, new_pos, cur_node.depth+1)
                    cur_node.add_child(child)
                    
                    # Set frontier
                    pair = (estimated_cost(child.depth, child, self.goal), child)
                    bisect.insort(frontier, pair)
                    
                    
                    if len(explorered_set) >= math.pow(b.size, 2):
                        return []
        return []


if __name__ == '__main__':
    b = board(8)
    p_start = position(0, 0)
    p_goal = position(2, 2)

    a = bfs(p_start, p_goal)
    path = a.search(b)
    b.print_pathway(path)
    print(a.expanded_node_count)

    a = dfs(p_start, p_goal)
    path = a.search(b)
    b.print_pathway(path)
    print(a.expanded_node_count)

    a = ids(p_start, p_goal)
    path = a.search(b)
    b.print_pathway(path)
    print(a.expanded_node_count)

    a = astar(p_start, p_goal)
    path = a.search(b)
    b.print_pathway(path)
    print(a.expanded_node_count)

    a = idastar(p_start, p_goal)
    path = a.search(b)
    b.print_pathway(path)
    print(a.expanded_node_count)