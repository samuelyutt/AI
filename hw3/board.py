import copy, random


class Board(object):
    def __init__(self, difficulty):
        init_param = {}
        if 'easy' == difficulty:
            init_param = {'size': (9, 9), 'mines': 10}
        elif 'medium' == difficulty:
            init_param = {'size': (16, 16), 'mines': 25}
        elif 'hard' == difficulty:
            init_param = {'size': (30, 16), 'mines': 99}
        
        self.x = init_param['size'][0]
        self.y = init_param['size'][1]
        self.mines = init_param['mines']
        self.hints = []
        
        # Randomly generate a new board
        positions = []
        for j in range(self.y):
            for i in range(self.x):
                positions.append((i, j))
        
        # Select mine positions
        mine_pos = random.sample(positions, self.mines)

        # 
        for j in range(self.y):
            for i in range(self.x):
                if i == 0:
                    self.hints.append([])
                if (i, j) in mine_pos:
                    self.hints[j].append(-3)
                else:
                    around = self.around_position((i, j))
                    mines_count = 0
                    for a in around:
                        if a in mine_pos:
                            mines_count += 1
                    self.hints[j].append(mines_count)
                

    def available_position(self, position):
        # Returns true if the given position is available on this board
        return 0 <= position[0] < self.x and 0 <= position[1] < self.y

    def around_position(self, position):
        # Returns a list of available postions around the given position
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
        # Return a list of current board status
        current = copy.deepcopy(self.hints)
        for variable in asgn_vrbls:
            x = variable.position[0]
            y = variable.position[1]
            if variable.assignment == 0:
                current[x][y] = -2
            elif variable.assignment == 1:
                current[x][y] = -3
        return current

    def print_board(self, asgn_vrbls = []):
        # Print the current board status
        # _     : Unassigned
        # |     : Assigned no mine
        # *     : Assigned mine
        # [0-8] : Hint
        current = self.current_board(asgn_vrbls)
        for j in range(self.y):
            for i in range(self.x):
                current[i][j] = '_' if current[i][j] == -1 else current[i][j]
                current[i][j] = '|' if current[i][j] == -2 else current[i][j]
                current[i][j] = '*' if current[i][j] == -3 else current[i][j]
                print(current[i][j], end=" ")
            print()


        

if __name__ == '__main__':
    b = Board('easy')
    b.print_board()