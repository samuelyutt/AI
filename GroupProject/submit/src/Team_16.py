
import STcpClient
import copy, math, random, time

'''
    輪到此程式移動棋子
    board : 棋盤狀態(list of list), board[i][j] = i row, j column 棋盤狀態(i, j 從 0 開始)
            0 = 空、1 = 黑、2 = 白、-1 = 四個角落
    is_black : True 表示本程式是黑子、False 表示為白子

    return Step
    Step : single touple, Step = (r, c)
            r, c 表示要下棋子的座標位置 (row, column) (zero-base)
'''

def GetStep(board, is_black):
    """
    Example:
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    return (x,y)
    """
    my_side = 1 if is_black else -1
    current_board = Board(board)
    movable = current_board.movable(my_side)
    my_step = MCTSAgent(side=my_side).take_action(current_board, movable)
    return (my_step[1], my_step[0])


while(True):
    (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
    if(stop_program):
        break

    Step = GetStep(board, is_black)
    STcpClient.SendStep(id_package, Step)

class Board():
    def __init__(self, board = []):
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
        if board:
            for i in range(8):
                for j in range(8):
                    self.status[i][j] = board[j][i] if board[j][i] != 2 else -1
            self.status[0][0] = 9
            self.status[0][7] = 9
            self.status[7][0] = 9
            self.status[7][7] = 9

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

    def is_over(self):
        black_movable = self.movable(1)
        white_movable = self.movable(-1)
        return len(black_movable) == 0 and len(white_movable) == 0

    def statistics(self):
        black_count = 0
        white_count = 0
        for j in range(self.size_y):
            for i in range(self.size_x):
                if self.status[i][j] == 1:
                    black_count += 1
                elif self.status[i][j] == -1:
                    white_count += 1
        return black_count, white_count 

    def available_position(self, position):
        x = position[0]
        y = position[1]
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def movable(self, side):
        movable_list = []
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.status[x][y] != 0:
                    continue
                if 0 < x < self.size_x-1 and 0 < y < self.size_y-1:
                    movable_list.append((x, y))
                else:
                    flip_pos = self.flip_positions(side, (x, y))
                    if len(flip_pos) == 0:
                        continue
                    movable_list.append((x, y))
        return movable_list

    def flip_positions(self, side, position):
        flip_list = []
        x = position[0]
        y = position[1]
        directions = [(-1, -1), (0, -1), (1, -1), 
                      (-1, 0),           (1, 0), 
                      (-1, 1),  (0, 1),  (1, 1)]
        for d in directions:
            tmp_list = []
            check_pos = (x, y)
            while True:
                check_pos = (check_pos[0] + d[0], check_pos[1] + d[1])
                if self.available_position(check_pos):
                    available = self.status[check_pos[0]][check_pos[1]] * side
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

    def flip(self, flip_positions):
        for f in flip_positions:
            self.status[f[0]][f[1]] *= -1

    def move(self, side, position):
        if position is None:
            return -1
        x = position[0]
        y = position[1]
        if self.status[x][y] != 0:
            return -1
        flip_pos = self.flip_positions(side, position)
        if 0 < x < self.size_x-1 and 0 < y < self.size_y-1:
            self.flip(flip_pos)
        else:
            if len(flip_pos) == 0:
                return -1
            self.flip(flip_pos)
        self.status[x][y] = side
        return 0

class Agent():
    def __init__(self, side = 0):
        self.side = side


class RandomAgent(Agent):
    def __init__(self, side = 0):
        super(RandomAgent, self).__init__(side)

    def __str__(self):
        return 'Random agent'

    def take_action(self, b, movable):
        action = None
        if len(movable):
            action = random.choice(movable)
        return action


class DullAgent(Agent):
    def __init__(self, side = 0):
        super(DullAgent, self).__init__(side)

    def __str__(self):
        return 'Dull agent'

    def take_action(self, b, movable):
        action = None
        flip_pos_count = -1
        if len(movable):
            action = movable[-1]
        return action


class GreedyAgent(Agent):
    def __init__(self, side = 0):
        super(GreedyAgent, self).__init__(side)

    def __str__(self):
        return 'Greedy agent'

    def take_action(self, b, movable):
        action = None
        flip_pos_count = -1
        if len(movable):
            for a in movable:
                tmp = len(b.flip_positions(self.side, a))
                if tmp > flip_pos_count:
                    action = a
                    flip_pos_count = tmp
        return action


class Human(Agent):
    def __init__(self, side = 0):
        super(Human, self).__init__(side)

    def __str__(self):
        return 'Human'

    def take_action(self, b, movable):
        action = None
        if len(movable):
            while True:
                decision = input('Enter a position: ').split()
                if len(decision) == 2:
                    action = (int(decision[0]), int(decision[1]))
                    if action in movable:
                        break
                print('Not an available move')
        return action


class Node():
    def __init__(self, board, side, tmp_side, action, parent):
        self.board = board
        self.untried_actions = self.board.movable(side)
        self.side = side
        self.tmp_side = tmp_side
        self.previous_action = action
        self.parent = parent
        self.children = []
        self.Q = 0
        self.N = 0

    def __str__(self):
        ret = '==== Node ===='
        ret += '\nQ: ' + str(self.Q)
        ret += '\nN: ' + str(self.N)
        ret += '\nside: ' + str(self.side)
        ret += '\ntmp_side: ' + str(self.tmp_side)
        ret += '\nprntprev_action: ' + (str(self.parent.previous_action) if not self.is_root() else str(None))
        ret += '\nprevious_action: ' + str(self.previous_action)
        ret += '\nchild: ' + str(len(self.children))
        ret += '\nuntried: ' + str(len(self.untried_actions))
        ret += '\nucb: ' + (str(self.UCB_value()) if not self.is_root() else str(None))
        return ret

    def is_root(self):
        return self.parent == None

    def is_leaf(self):
        return len(self.children) == 0

    def UCB_value(self, C = 1.4):
        # return self.Q / self.N + C * math.sqrt(2 * math.log(self.parent.N) / self.N) if self.N else 9999.9
        return self.Q / self.N + C * math.sqrt(math.log(self.parent.N) / self.N) if self.N else 9999.9

    def select(self, C = 1.4):
        max_UCB_value = None
        select_c = None
        for c in self.children:
            UCB_value = c.UCB_value(C)
            if max_UCB_value == None or UCB_value > max_UCB_value:
                max_UCB_value = UCB_value
                select_c = c
        return select_c

    def expand(self):
        action = self.untried_actions.pop()
        next_board = copy.deepcopy(self.board)
        next_board.move(self.tmp_side, action)
        child = Node(next_board, self.side, self.tmp_side * -1, action, self)
        self.children.append(child)
        return child

    def update(self, winner_side):
        self.N += 1
        if winner_side == self.side:
            self.Q += 1
        elif winner_side == self.side * -1:
            self.Q -= 1
        if not self.is_root():
            self.parent.update(winner_side)

    def rollout(self):
        tmp_board = copy.deepcopy(self.board)
        side = self.tmp_side
        stuck_count = 0
        while True:
            movable = tmp_board.movable(side)
            if len(movable):
                action = random.choice(movable)
                tmp_board.move(side, action)
                stuck_count = 0
            else:
                stuck_count += 1
            if stuck_count == 2:
                black_count, white_count = tmp_board.statistics()
                result = black_count - white_count
                if result > 0:
                    return 1
                elif result < 0:
                    return -1
                elif result == 0:
                    return 0
                break
            side *= -1


class MCTSAgent(Agent):
    def __init__(self, iteration_count = 200, side = 0, type_ = 2):
        super(MCTSAgent, self).__init__(side)
        self.iteration_count = iteration_count
        self.type = type_

    def __str__(self):
        return 'MCTS agent (' + str(self.iteration_count) + ')'

    def iteration(self, root):
        start = time.time()
        # for _ in range(self.iteration_count):
        while time.time() - start < 4.6:
            rollout_node = self.selection2(root) if self.type == 2 else self.selection(root)
            result = self.simulation(rollout_node)
            self.backpropagation(rollout_node, result)
        return root.select(0.0)

    def selection(self, root):
        current_node = root
        if len(current_node.untried_actions):
            current_node = self.expansion(current_node)
        else:
            while not current_node.is_leaf():
                current_node = current_node.select()
        return current_node
        
    def selection2(self, root):
        current_node = root
        while True:
            if len(current_node.untried_actions):
                current_node = self.expansion(current_node)
                break
            if current_node.is_leaf():
                break
            current_node = current_node.select()
        return current_node

    def expansion(self, node):
        new_node = node.expand()
        return new_node

    def simulation(self, node):
        result = node.rollout()
        return result

    def backpropagation(self, node, result):
        node.update(result)

    def take_action(self, b, movable):
        action = None
        if len(movable):
            root = Node(copy.deepcopy(b), self.side, self.side, None, None)
            select_node = self.iteration(root)
            action = select_node.previous_action
            # for c in root.children:
            #     print(c)
            #     print(c.UCB_value(0.0))
            # if not select_node.is_leaf():
            #     print('cc')
            #     for cc in select_node.children:
            #         print(cc)
        return action


