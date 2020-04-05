"""
    This program defines the framwork of the board
"""

import math


class board:
    def __init__(self, size_):
        self.size = size_

    def print_pathway(self, path_list):
        # This function prints the path from the starting
        # position to the goal position on this board
        # with no return value
        ls = []
        for i in range(int(math.pow(self.size, 2))):
            ls.append("  +")
        for i in range(len(path_list)):
            pos = path_list[i]
            if i == 0:
                ls[ pos.y * self.size + pos.x ] = "  S"
            elif i == len(path_list) - 1:
                ls[ pos.y * self.size + pos.x ] = "  G"
            else:
                ls[ pos.y * self.size + pos.x ] = "{: 3}".format(i)
        print("   ", end="")
        for i in range(self.size):
            print("{: 3}".format(i), end="")
        print()
        for i in range(int(math.pow(self.size, 2))):
            if not i % self.size:
                print("{: 3}".format(int(i/self.size)), end="")
            print(ls[i], end="")
            if not (i+1) % self.size:
                print()


class move:
    def __init__(self, move_x = 0, move_y = 0):
        self.x = move_x
        self.y = move_y


class position:
    def __init__(self, position_x = -1, position_y = -1):
        self.x = position_x
        self.y = position_y

    def __str__(self):
        return ("({}, {})" .format(str(self.x), str(self.y)))

    def __repr__(self):
        return self.__str__

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not ( __eq__(self, other) )

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def is_available_pos(self, b):
        # This function returns True if this position is
        # available on the given board; otherwise False
        return 0 <= self.x < b.size and 0 <= self.y < b.size

    def available_moves(self, b):
        # This function returns a list of all possible
        # positions on the given board after taking 
        # a single move from this position 
        new_pos_list = []
        moves = [move(-1, -2), move(1, -2), move(-2, -1), move(2, -1), move(-2, 1), move(2, 1), move(-1, 2), move(1, 2)]

        for mv in moves:
            new_x = self.x + mv.x
            new_y = self.y + mv.y
            new_pos = position(new_x, new_y)
            if new_pos.is_available_pos(b):
                new_pos_list.append(new_pos)

        return new_pos_list


if __name__ == '__main__':
    # Examples
    b = board(8)
    p = position(5, 5)
    next_p = p.available_moves(b)
    for n in next_p:
        print(n)