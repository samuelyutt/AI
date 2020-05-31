class Board():
    def __init__(self):
        self.size_x = 8
        self.size_y = 8
        self.status = [[9, 0, 0, 0, 0, 0, 0, 9],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [9, 0, 0, 0, 0, 0, 0, 9]]

    def __str__(self):
        ret = '  0 1 2 3 4 5 6 7\n'
        for j in range(self.size_y):
            ret += str(j) + ' '
            for i in range(self.size_x):
                if self.status[i][j] == 0:
                    ret += '_'
                elif self.status[i][j] == 1:
                    ret += 'O'
                elif self.status[i][j] == -1:
                    ret += 'X'
                elif self.status[i][j] == 9:
                    ret += ' '
                ret += ' '
            ret += '\n'
        return ret

    def available_position(self, position):
        x = position[0]
        y = position[1]
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def flip(self, flip_positions):
        for f in flip_positions:
            self.status[f[0]][f[1]] *= -1

    def flip_positions(self, player, position):
        flip_list = []
        x = position[0]
        y = position[1]
        directions = [(-1, -1), (0, -1), (1, -1), 
                     (-1, 0),           (1, 0), 
                     (-1, 1), (0, 1), (1, 1)]
        for d in directions:
            tmp_list = []
            check_pos = (x, y)
            while True:
                check_pos = (check_pos[0] + d[0], check_pos[1] + d[1])
                if self.available_position(check_pos):
                    available = self.status[check_pos[0]][check_pos[1]] * player
                    # print(check_pos, available)
                    if available == 1:
                        flip_list += tmp_list
                        break
                    elif available == -1:
                        tmp_list.append(check_pos)
                    else:
                        break
                else:
                    break
        return flip_list



    def move(self, player, position):
        x = position[0]
        y = position[1]
        if self.status[x][y] != 0:
            return -1
        flip_pos = self.flip_positions(player, position)
        if 0 < x < self.size_x-1 and 0 < y < self.size_y-1:
            self.flip(flip_pos)
        else:
            if len(flip_pos) == 0:
                return -1
            self.flip(flip_pos)
        self.status[x][y] = player
        return 0

if __name__ == '__main__':
    b = Board()
    # b.status[3][3] = 1
    # b.status[3][4] = -1
    # b.status[4][3] = -1
    # b.status[4][4] = 1
    print(b)
    # tmp = b.flip_positions(1, (3, 5))
    # print(tmp)
    # b.move(1, (3, 5))
    # print(b)
    # b.move(-1, (3, 2))
    # print(b)
    # b.move(-1, (3, 6))
    # print(b)
    # b.move(-1, (2, 4))
    # print(b)
    # b.move(1, (1, 5))
    # print(b)
    # b.move(1, (4, 2))
    # print(b)

    # b.move(-1, (0, 6))
    # print(b)
    # b.move(-1, (5, 1))
    # print(b)
    # b.move(-1, (0, 6))
    # print(b)
    # b.move(-1, (0, 0))
    # print(b)

    # b.move(1, (2, 2))
    # print(b)
    

    # b.move(1, (1, 1))
    # print(b)

    # b.move(-1, (0, 0))
    # print(b)
    # b.move(-1, (5, 5))
    # print(b)
    # b.move(1, (6, 0))
    # print(b)
    # b.move(-1, (5, 3))
    # print(b)
    # b.move(-1, (2, 3))
    # print(b)

    

    for i in range(1, 6):
        b.move(-1, (1, i))
        b.move(-1, (5, i))

    for i in range(1, 6):
        b.move(-1, (i, 1))
        b.move(-1, (i, 5))

    for i in range(2, 5):
        b.move(1, (2, i))
        b.move(1, (4, i))

    for i in range(2, 5):
        b.move(1, (i, 2))
        b.move(1, (i, 4))


    print(b)

    b.move(-1, (3, 3))
    print(b)