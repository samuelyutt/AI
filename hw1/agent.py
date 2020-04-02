from board import position
from tree import node


class agent:
    def __init__(self, type, start_, goal_):
        self.algorithm = type
        self.start = start_
        self.goal = goal_

    def search(self):
        if self.algorithm == 0:
            return self.bfs()

    def bfs(self):        
        cur_node = node(None, self.start)

        explorered_set = []
        frontier = [cur_node]
        
        while len(frontier):            
            cur_node = frontier[0]
            possible_moves = cur_node.position.available_moves()

            for new_pos in possible_moves:
                if new_pos not in explorered_set:
                    child = node(cur_node, new_pos)
                    cur_node.add_child(child)
                    frontier.append(child)
                    explorered_set.append(new_pos)
                    if new_pos == self.goal:
                        tmp_node = child
                        while tmp_node != None:
                            print(tmp_node.position)
                            tmp_node = tmp_node.parent
                        break

            frontier.pop(0)


        return 0


if __name__ == '__main__':
    a = agent(0, position(0, 0), position(2, 2))
    print(a.search())