import copy
from variable import Variable


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

    def available_position(self, position):
        return 0 <= position[0] < self.size_x and 0 <= position[1] < self.size_y

    def around_position(self, position):
        x = position[0]
        y = position[1]
        psb_pos = [(x-1, y-1), (x, y-1), (x+1, y-1), 
                   (x-1, y),             (x+1, y), 
                   (x-1, y+1), (x, y+1), (x+1, y+1)]
        around = []
        for pos in psb_pos:
            if self.available_position(pos):
                around.append(pos)
        return around

    def current_board(self, asgn_vrbls = []):
        current = copy.deepcopy(self.hints)
        for variable in asgn_vrbls:
            x = variable.position[0]
            y = variable.position[1]
            current[x][y] = '|' if variable.assignment == 0 else current[x][y]
            current[x][y] = '*' if variable.assignment == 1 else current[x][y]
        return current

    def print_board(self, asgn_vrbls = []):
        current = self.current_board(asgn_vrbls)
        for j in range(self.size_y):
            for i in range(self.size_x):
                current[i][j] = '_' if current[i][j] == -1 else current[i][j]
                print(current[i][j], end=" ")
            print()
    
    def forward_checking_limit(self, asgn_vrbls, position):
        current = self.current_board(asgn_vrbls)
        lower_bound = 0
        upper_bound = 0
        around = self.around_position(position)
        for a in around:
            if current[a[0]][a[1]] == '*':
                lower_bound += 1
                upper_bound += 1
            elif current[a[0]][a[1]] == -1:
                upper_bound += 1
        return lower_bound, upper_bound

    def arc_consistent_check(self, asgn_vrbls, position):
        x = position[0]
        y = position[1]
        if not self.available_position(position):
            return 0
        if self.hints[x][y] == -1:
            return 0
        
        current = self.current_board(asgn_vrbls)
        
        bombs_count = 0
        around = self.around_position(position)
        for a in around:
            if current[a[0]][a[1]] == '*':
                bombs_count += 1

        return self.hints[x][y] - bombs_count

    def global_constraint_check(self, asgn_vrbls):
        mines_count = 0
        for variable in asgn_vrbls:
            if variable.assignment == 1:
                mines_count += 1

        return self.mines_count - mines_count


if __name__ == '__main__':
    inputs = '6 6 10 -1 -1 -1 1 1 -1 -1 3 -1 -1 -1 0 2 3 -1 3 3 2 -1 -1 2 -1 -1 -1 -1 2 2 3 -1 3 -1 1 -1 -1 -1 1'
    b = Board(inputs)
    
    variables = []
    for j in range(b.size_y):
        for i in range(b.size_x):
            if b.hints[i][j] == -1:
                variables.append(Variable(i, j))

    b.print_board(variables)
    print(b.arc_consistent_check(variables, (5, 1)))
    print(b.arc_consistent_check(variables, (0, 0)))


