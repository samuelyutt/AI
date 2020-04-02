import queue
import bisect
from board import board
from board import position
from tree import node

def estimated_cost(g, node, goal):
    pos = node.position
    heuristic = int( (abs(pos.x-goal.x)+abs(pos.y-goal.y)) / 3 )
    return g + heuristic

def path_list(goal_node):
    ret = []
    tmp_node = goal_node
    while tmp_node != None:
        ret.append(tmp_node.position)
        tmp_node = tmp_node.parent
    ret.reverse()
    return ret


class agent:
    def __init__(self, start_, goal_):
        self.node_count = 0
        self.start = start_
        self.goal = goal_


class bfs(agent):
    def __init__(self, start_, goal_):
        super(bfs, self).__init__(start_, goal_)

    def search(self, b):
        root = node(None, self.start)
        self.node_count += 1

        explorered_set = []
        frontier = queue.Queue(maxsize = -1)
        frontier.put(root)
        
        while not frontier.empty():            
            cur_node = frontier.get()
            possible_moves = cur_node.position.available_moves(b)

            for new_pos in possible_moves:
                if new_pos not in explorered_set:
                    child = node(cur_node, new_pos)
                    cur_node.add_child(child)
                    self.node_count += 1
                    frontier.put(child)
                    explorered_set.append(new_pos)
                    if new_pos == self.goal:
                        return path_list(child)                        
        return []


class dfs(agent):
    def __init__(self, start_, goal_):
        super(dfs, self).__init__(start_, goal_)

    def search(self, b):
        root = node(None, self.start)
        self.node_count += 1

        explorered_set = []
        frontier = [root]
        
        while len(frontier):            
            cur_node = frontier.pop()
            possible_moves = cur_node.position.available_moves(b)

            for new_pos in possible_moves:
                if new_pos not in explorered_set:
                    child = node(cur_node, new_pos)
                    cur_node.add_child(child)
                    frontier.append(child)
                    self.node_count += 1
                    explorered_set.append(new_pos)
                    if new_pos == self.goal:
                        return path_list(child)
        return []


class ids(agent):
    def __init__(self, start_, goal_):
        super(ids, self).__init__(start_, goal_)

    def search(self, b):
        depth_limit = -1

        while True:
            depth_limit += 1

            root = node(None, self.start, 0)
            self.node_count += 1

            explorered_set = []
            frontier = [root]
            
            while len(frontier):            
                cur_node = frontier.pop()
                if cur_node.depth == depth_limit:
                    continue
                possible_moves = cur_node.position.available_moves(b)

                for new_pos in possible_moves:
                    if new_pos not in explorered_set:
                        child = node(cur_node, new_pos, cur_node.depth+1)
                        cur_node.add_child(child)
                        frontier.append(child)
                        self.node_count += 1
                        explorered_set.append(new_pos)
                        if new_pos == self.goal:
                            return path_list(child)
        return []


class astar(agent):
    def __init__(self, start_, goal_):
        super(astar, self).__init__(start_, goal_)

    def search(self, b):
        root = node(None, self.start, 0)
        self.node_count += 1

        explorered_set = []
        frontier = []
        pair = (estimated_cost(root.depth, root, self.goal), root)
        bisect.insort(frontier, pair)
        
        while len(frontier):            
            cur_node = frontier.pop(0)[1]
            possible_moves = cur_node.position.available_moves(b)

            for new_pos in possible_moves:
                if new_pos not in explorered_set:
                    child = node(cur_node, new_pos, cur_node.depth+1)
                    cur_node.add_child(child)
                    pair = (estimated_cost(child.depth, child, self.goal), child)
                    bisect.insort(frontier, pair)
                    self.node_count += 1
                    explorered_set.append(new_pos)
                    if new_pos == self.goal:
                        return path_list(child)
        return []


class idastar(agent):
    def __init__(self, start_, goal_):
        super(idastar, self).__init__(start_, goal_)

    def search(self, b):
        depth_limit = -1

        while True:
            depth_limit += 1

            root = node(None, self.start, 0)
            self.node_count += 1

            explorered_set = []
            frontier = []
            pair = (estimated_cost(root.depth, root, self.goal), root)
            bisect.insort(frontier, pair)
            
            while len(frontier):            
                cur_node = frontier.pop(0)[1]
                if cur_node.depth == depth_limit:
                    continue
                possible_moves = cur_node.position.available_moves(b)

                for new_pos in possible_moves:
                    if new_pos not in explorered_set:
                        child = node(cur_node, new_pos, cur_node.depth+1)
                        cur_node.add_child(child)
                        pair = (estimated_cost(child.depth, child, self.goal), child)
                        bisect.insort(frontier, pair)
                        self.node_count += 1
                        explorered_set.append(new_pos)
                        if new_pos == self.goal:
                            return path_list(child)
        return []


if __name__ == '__main__':
    b = board(8)
    p_start = position(0, 0)
    p_goal = position(2, 2)

    a = bfs(p_start, p_goal)
    path = a.search(b)
    b.print_pathway(path)
    print(a.node_count)

    a = dfs(p_start, p_goal)
    path = a.search(b)
    b.print_pathway(path)
    print(a.node_count)

    a = ids(p_start, p_goal)
    path = a.search(b)
    b.print_pathway(path)
    print(a.node_count)

    a = astar(p_start, p_goal)
    path = a.search(b)
    b.print_pathway(path)
    print(a.node_count)

    a = idastar(p_start, p_goal)
    path = a.search(b)
    b.print_pathway(path)
    print(a.node_count)