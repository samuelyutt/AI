# from variable import Variable


class Board():
    def __init__(self, inputs):
        args = inputs.split()
        self.size_x = int(args[0])
        self.size_y = int(args[1])
        self.mines_count = int(args[2])
        self.hints = []

        idx = 3
        for i in range(self.size_y):
            for j in range(self.size_x):
                if i == 0:
                    self.hints.append([])
                self.hints[j].append(int(args[idx]))
                idx += 1

    def print_board(self, variables = []):
        outputs = self.hints
        for variable in variables:
            x = variable.x
            y = variable.y
            outputs[x][y] = '_' if variable.assignment == -1 else outputs[x][y]
            outputs[x][y] = '|' if variable.assignment == 0 else outputs[x][y]
            outputs[x][y] = '*' if variable.assignment == 1 else outputs[x][y]
        for j in range(self.size_y):
            for i in range(self.size_x):
                print(outputs[i][j], end=" ")
            print()


if __name__ == '__main__':
    inputs = '6 6 10 -1 -1 -1 1 1 -1 -1 3 -1 -1 -1 0 2 3 -1 3 3 2 -1 -1 2 -1 -1 -1 -1 2 2 3 -1 3 -1 1 -1 -1 -1 1'
    b = Board(inputs)
    print(b.size_x)
    print(b.size_y)
    print(b.mines_count)
    for j in range(b.size_y):
        for i in range(b.size_x):
            print(b.hints[i][j], end=" ")
        print()