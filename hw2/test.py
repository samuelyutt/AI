import time, random
from board import Board
from agent import Agent

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


if __name__ == '__main__':
    inputs = gen_board(board_x = 16, board_y = 16, mines = 50, hints = 100)
    start_time = time.time()

    a = Agent(forward_checking = True, mrv = True, heuristic = 'space', lcv = False)
    
    # for inputs in inputs_list:
    b = Board(inputs)
    result = a.search(b)
    b.print_board(result)
    print()

    search_time = (time.time() - start_time) * 100
    print(search_time)