from board import Board


class Variable():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.assignment = -1
        self.domain = [0, 1]

if __name__ == '__main__':
    variables = []

    inputs = '6 6 10 -1 -1 -1 1 1 -1 -1 3 -1 -1 -1 0 2 3 -1 3 3 2 -1 -1 2 -1 -1 -1 -1 2 2 3 -1 3 -1 1 -1 -1 -1 1'
    b = Board(inputs)
    
    for j in range(b.size_y):
        for i in range(b.size_x):
            if b.hints[i][j] == -1:
                variables.append(Variable(i, j))

    b.print_board(variables)
