import time
from board import board
from board import position
from agent import agent
from agent import bfs
from agent import dfs
from agent import ids
from agent import astar
from agent import idastar

def algorithm_type():
    print("======== Algorithm type comparision ========")
    
    b = board(8)
    pairs = [(position(0, 0), position(2, 2)), 
             (position(2, 2), position(0, 0)), 
             (position(0, 0), position(7, 7)), 
             (position(7, 7), position(0, 0)), 
             (position(0, 0), position(0, 1)), 
             (position(0, 1), position(0, 0))]
    
    for pair in pairs:
        p_start = pair[0]
        p_goal = pair[1]
        agents = [bfs(p_start, p_goal), dfs(p_start, p_goal), ids(p_start, p_goal), astar(p_start, p_goal), idastar(p_start, p_goal)]
        bm = [-1, -1, -1]

        print("From", p_start, "to", p_goal)
        print("Algorithm\tSearch time\t\tSteps\t\tExpanded nodes")
        for a in agents:
            start_time = time.time()
            path = a.search(b)
            search_time = (time.time() - start_time) * 100
            steps = len(path) - 1

            bm[0] = search_time if bm[0] == -1 else bm[0]
            bm[1] = steps if bm[1] == -1 else bm[1]
            bm[2] = a.expanded_node_count if bm[2] == -1 else bm[2]

            print("{}\t\t{:.6f} ({:.3f})\t{} ({:.3f})\t{} ({:.3f})" .format(a, search_time, search_time/bm[0], steps, steps/bm[1], a.expanded_node_count, a.expanded_node_count/bm[2]))
        print()

def board_size():
    print("======== Board size comparision ========")
    
    p_start = position(0, 0)
    p_goal = position(2, 2)
    agents = [bfs(p_start, p_goal), dfs(p_start, p_goal), ids(p_start, p_goal), astar(p_start, p_goal), idastar(p_start, p_goal)]
    
    for a in agents:
        print(a)
        print("Board size\tSearch time\t\tSteps\t\tExpanded nodes")
        bm = [-1, -1, -1, -1]

        for b_size in range(3, 16):
            b = board(b_size)
                    
            start_time = time.time()
            path = a.search(b)
            search_time = (time.time() - start_time) * 100
            steps = len(path) - 1

            bm[0] = b_size if bm[0] == -1 else bm[0]
            bm[1] = search_time if bm[1] == -1 else bm[1]
            bm[2] = steps if bm[2] == -1 else bm[2]
            bm[3] = a.expanded_node_count if bm[3] == -1 else bm[3]

            print("{} ({:.3f})\t{:.6f} ({:.3f})\t{} ({:.3f})\t{} ({:.3f})" .format(b_size, b_size/bm[0], search_time, search_time/bm[1], steps, steps/bm[2], a.expanded_node_count, a.expanded_node_count/bm[3]))
        print()


if __name__ == '__main__':
    algorithm_type()
    
