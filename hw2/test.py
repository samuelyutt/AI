import time, random
from board import Board
from agent import Agent

FFNF = Agent(forward_checking = False, mrv = False, heuristic = '', lcv = False)
TFNF = Agent(forward_checking = True, mrv = False, heuristic = '', lcv = False)

TTNF = Agent(forward_checking = True, mrv = True, heuristic = '', lcv = False)
TFDF = Agent(forward_checking = True, mrv = False, heuristic = 'degree', lcv = False)
TFSF = Agent(forward_checking = True, mrv = False, heuristic = 'space', lcv = False)
TFNT = Agent(forward_checking = True, mrv = False, heuristic = '', lcv = True)

TTDF = Agent(forward_checking = True, mrv = True, heuristic = 'degree', lcv = False)
TTSF = Agent(forward_checking = True, mrv = True, heuristic = 'space', lcv = False)
TTNT = Agent(forward_checking = True, mrv = True, heuristic = '', lcv = True)

TTDT = Agent(forward_checking = True, mrv = True, heuristic = 'degree', lcv = True)
TTST = Agent(forward_checking = True, mrv = True, heuristic = 'space', lcv = True)


def around_position(position, board_x, board_y):
    around = []
    if position == 0:
        around = [ 
                                                         position+1, 
                                       position+board_x, position+board_x+1]
    elif position+1 == board_x:
        around = [
                   position-1,
                   position+board_x-1, position+board_x]
    elif position == board_x*(board_y-1):
        around = [                     position-board_x, position-board_x+1, 
                                                         position+1, 
                  ]
    elif position+1 == board_x*board_y:
        around = [ position-board_x-1, position-board_x, 
                   position-1, 
                  ]
    elif 0 < position < board_y:
        around = [ 
                   position-1,                           position+1, 
                   position+board_x-1, position+board_x, position+board_x+1]
    elif position % board_x == 0:
        around = [                     position-board_x, position-board_x+1, 
                                                         position+1, 
                                       position+board_x, position+board_x+1]
    elif (position+1) % board_x == 0:
        around = [ position-board_x-1, position-board_x,
                   position-1, 
                   position+board_x-1, position+board_x]
    elif board_x*(board_y-1) < position < board_x*board_y:
        around = [ position-board_x-1, position-board_x, position-board_x+1, 
                   position-1,                           position+1, 
                  ]
    else:
        around = [ position-board_x-1, position-board_x, position-board_x+1, 
                   position-1,                           position+1, 
                   position+board_x-1, position+board_x, position+board_x+1]    
    return around

def gen_board(board_x, board_y, mines, hints):
    # Randomly generate a new board
    board_inputs = []
    positions = []
    for i in range(board_x * board_y):
        board_inputs.append(-1)
        positions.append(i)

    # Select positions
    sltd_pos = random.sample(positions, mines + hints)
    mine_pos = sltd_pos[0:mines]
    hint_pos = sltd_pos[mines:]
    
    for pos in hint_pos:
        around = around_position(pos, board_x, board_y)
        mines_count = 0
        for a in around:
            if a in mine_pos:
                mines_count += 1
        board_inputs[pos] = mines_count

    # Generate inputs string
    board_inputs_string = str(board_x) + ' ' + str(board_y) + ' ' + str(mines)
    for i in board_inputs:
        board_inputs_string += ' ' + str(i)
    return board_inputs_string

def algorithm_test(board_counts, board_x, board_y, mines, hints, agents):
    print()
    print('Test with   :', board_counts, 'boards')
    print('Board size  :', board_x, '*', board_y)
    print('Mines       :', mines)
    print('Hints       :', hints)
    print()
    print('FwCheck\tMRV\tHeurs\tLCV\tTime per board (ms)')
    print('---------------------------------------------------------')

    inputs_list = []
    for i in range(board_counts):
        inputs_list.append(gen_board(board_x, board_y, mines, hints))

    for a in agents:
        start_time = time.time()
        for inputs in inputs_list:
            b = Board(inputs)
            a.search(b)
        search_time = (time.time() - start_time) * 1000
        print('{}\t{}\t{}\t{}\t{}'.format(a.fc, a.mrv, a.heuristic if a.heuristic != '' else 'None', a.lcv, search_time / board_counts))
    print()

def board_size_test(board_counts, min_board_size, max_board_size, agents):
    for a in agents:
        print()
        print('Test with       :', board_counts, 'boards per board size')
        print('Mines ratio     :', mines_ratio)
        print('Hints ratio     :', hints_ratio)
        print('Using algorithm : FwCheck\tMRV\tHeurs\tLCV')
        print('                  {}\t\t{}\t{}\t{}'.format(a.fc, a.mrv, a.heuristic if a.heuristic != '' else 'None', a.lcv))
        print()
        print('Board size\tTime per board (ms)')
        print('---------------------------------------------------------')
        
        for board_size in range(min_board_size, max_board_size+1):
            inputs_list = []
            mines = int(board_size * board_size * mines_ratio)
            hints = int(board_size * board_size * hints_ratio)
            
            for i in range(board_counts):
                inputs_list.append(gen_board(board_size, board_size, mines, hints))

            start_time = time.time()
            for inputs in inputs_list:
                b = Board(inputs)
                a.search(b)
            search_time = (time.time() - start_time) * 1000

            print('{: 3} *{: 3}\t{}'.format(board_size, board_size, search_time / board_counts))

        print()

if __name__ == '__main__':
    # Settings
    board_counts = 100

    #### For algorithm test
    board_x = 6
    board_y = 6
    mines = 10
    hints = 16
    agents = [TTDF]
    # agents = [FFNF, TFNF]
    # agents = [TFNF, TTNF, TFDF, TFSF, TFNT]
    # agents = [TTNF, TTDF, TTSF, TTNT]
    # agents = [TTNF, TTDT, TTST, TTNT]
    
    #### For board size test
    min_board_size = 4
    max_board_size = 12
    mines_ratio = 0.28
    hints_ratio = 0.44
    agents = [TTNF, TTNT, TTDF, TTSF, TTDT, TTST]
    
    
    # Tests
    # algorithm_test(board_counts, board_x, board_y, mines, hints, agents)    
    board_size_test(board_counts, min_board_size, max_board_size, agents)
    
