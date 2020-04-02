global size

size = 8

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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not ( __eq__(self, other) )

    def available_moves(self):
        global size
        new_pos = []
        moves = [move(-1, -2), move(1, -2), move(-2, -1), move(2, -1), move(-2, 1), move(2, 1), move(-1, 2), move(1, 2)]

        for mv in moves:
            new_x = self.x + mv.x
            new_y = self.y + mv.y
            if 0 <= new_x < size and 0 <= new_y < size:
                new_pos.append(position(new_x, new_y))

        return new_pos


if __name__ == '__main__':
    p = position(5, 5)
    next_p = p.available_moves()
    for n in next_p:
        print(n.x, n.y)