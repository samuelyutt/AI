import copy, math, random


class Action:
    def __init__(self, action, position = None):
        self.action = action
        self.position = position


class Board():
    def __init__(self, difficulty):
        init_param = {}
        if 'easy' == difficulty:
            init_param = {'size': (9, 9), 'mines': 10}
        elif 'medium' == difficulty:
            init_param = {'size': (16, 16), 'mines': 40}
        elif 'hard' == difficulty:
            init_param = {'size': (30, 16), 'mines': 99}
        
        self.x = init_param['size'][0]
        self.y = init_param['size'][1]
        self.mines = init_param['mines']
        self.hints = []
        self.marked = []
        
        # Randomly generate a new board
        positions = []
        for j in range(self.y):
            for i in range(self.x):
                positions.append((i, j))
        
        # Select mine and initial safe positions
        init_safe_cells = round(math.sqrt(self.x * self.y)) 
        sltd_pos = random.sample(positions, self.mines + init_safe_cells)
        mine_pos = sltd_pos[0:self.mines]
        self.init_safe_pos = sltd_pos[self.mines:]
        # print(mine_pos)
        # print(self.init_safe_pos)

        # Generate hints
        for i in range(self.x):
            for j in range(self.y):
                if j == 0:
                    self.hints.append([])
                    self.marked.append([])
                if (i, j) in mine_pos:
                    self.hints[i].append(-3)
                else:
                    around = self.around_position((i, j))
                    mines_count = 0
                    for a in around:
                        if a in mine_pos:
                            mines_count += 1
                    self.hints[i].append(mines_count)
                self.marked[i].append(0)
                
    def query(self, position):
        x = position[0]
        y = position[1]
        self.marked[x][y] = -2
        return self.hints[x][y]

    def mark_mine(self, position):
        x = position[0]
        y = position[1]
        self.marked[x][y] = -3    

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

    def around_unmarked_position(self, position):
        # Returns a list of unmarked postions around the given position
        around = self.around_position(position)
        around_unmarked = []
        for a in around:
            if self.marked[a[0]][a[1]] == 0:
                around_unmarked.append(a)
        return around_unmarked

    def around_marked_mine_position(self, position):
        # Returns a list of marked mine postions around the given position
        around = self.around_position(position)
        around_marked_mine = []
        for a in around:
            if self.marked[a[0]][a[1]] == -3:
                around_marked_mine.append(a)
        return around_marked_mine

    def check_success(self):
        marked_count = 0
        marked_mine_count = 0
        current = copy.deepcopy(self.marked)
        for j in range(self.y):
            for i in range(self.x):
                if current[i][j] != 0:
                    marked_count += 1
                if current[i][j] == -3:
                    marked_mine_count += 1
        return marked_count == self.x*self.y and marked_mine_count == self.mines

    def print_current_board(self):
        # Print the current board status
        # _     : Unassigned
        # |     : Assigned no mine
        # *     : Assigned mine
        # [0-8] : Hint
        current = copy.deepcopy(self.marked)
        for j in range(self.y):
            for i in range(self.x):
                current[i][j] = '_' if current[i][j] == 0 else current[i][j]
                current[i][j] = self.hints[i][j] if current[i][j] == -2 else current[i][j]
                current[i][j] = '*' if current[i][j] == -3 else current[i][j]
                print(current[i][j], end=" ")
            print()

    def print_answer_board(self):
        # Print the answer board
        # *     : Mine
        # [0-8] : Hint
        board = copy.deepcopy(self.hints)
        for j in range(self.y):
            for i in range(self.x):
                board[i][j] = '*' if board[i][j] == -3 else board[i][j]
                print(board[i][j], end=" ")
            print()


        

if __name__ == '__main__':
    b = Board('easy')
    b.print_board()