"""
    This is the main program
    Usage: knight.py <algorithm> <starting_x> <starting_y> <goal_x> <goal_y>
        0   BFS
        1   DFS
        2   IDS
        3   A*
        4   IDA*
"""

import sys
from board import board
from board import position
from agent import agent
from agent import bfs
from agent import dfs
from agent import ids
from agent import astar
from agent import idastar

def usage():
    print("usage: knight.py <algorithm> <starting_x> <starting_y> <goal_x> <goal_y>")
    print("\t0\tBFS")
    print("\t1\tDFS")
    print("\t2\tIDS")
    print("\t3\tA*")
    print("\t4\tIDA*")
    return

""" This is the main function of the program """
def knight(algorithm_type, starting_x, starting_y, goal_x, goal_y):
    # Create a board of size 8
    b = board(8)

    # Set starting position and goal position
    p_start = position(starting_x, starting_y)
    p_goal = position(goal_x, goal_y)

    # Check if the positions are available
    if not p_start.is_available_pos(b) or not p_goal.is_available_pos(b):
        print("position out of board range")
        return

    # Create agent
    a = agent(p_start, p_goal)
    
    # Classify the type of agent
    if algorithm_type == 0:
        a = bfs(p_start, p_goal)
    elif algorithm_type == 1:
        a = dfs(p_start, p_goal)
    elif algorithm_type == 2:
        a = ids(p_start, p_goal)
    elif algorithm_type == 3:
        a = astar(p_start, p_goal)
    elif algorithm_type == 4:
        a = idastar(p_start, p_goal)
    else:
        usage()
        return

    # Search path
    path_list = a.search(b)

    # Print path
    for path in path_list:
        print(path, end="")
    print()

    # Return the number of expanded nodes
    return a.expanded_node_count


if __name__ == '__main__':
    if len(sys.argv) != 6:
        usage()
    else:
        algorithm_type = int(sys.argv[1])
        starting_x = int(sys.argv[2])
        starting_y = int(sys.argv[3])
        goal_x = int(sys.argv[4])
        goal_y = int(sys.argv[5])

        knight(algorithm_type, starting_x, starting_y, goal_x, goal_y)

