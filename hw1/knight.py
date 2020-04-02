global size

size = 8

class pair:
    def __init__(self, position_x = 0, position_y = 0):
        self.x = position_x
        self.y = position_y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not ( __eq__(self, other) )


class board:
    def __init__(self):
        pass

    def available_moves(self, position):
        moves = []
        dirs = [pair(-1, -2), pair(1, -2), pair(-2, -1), pair(2, -1), pair(-2, 1), pair(2, 1), pair(-1, 2), pair(1, 2)]
        no_move = pair()

        if 
		