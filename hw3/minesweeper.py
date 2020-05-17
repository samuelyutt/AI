import time
from board import Board, Action
from logic import Literal, Clause
from agent import Agent


if __name__ == '__main__':
    b = Board('easy')
    a = Agent()
    start_time = time.time()
    
    # Initial
    for pos in b.init_safe_pos:
        new_clause = Clause( [-Literal(pos)] )
        a.add_clause_to_KB(new_clause)
    
    while True:
        # Print current board
        b.print_current_board()
        print()

        # Take action
        action = a.take_action(b)
        
        # Game flow
        if 'query' == action.action:
            new_hint = b.query(action.position)
            if new_hint == -3:
                print('Fail on', action.position)
                break
            a.new_hint(action.position, new_hint, b)
        elif 'mark_mine' == action.action:
            b.mark_mine(action.position)
        elif 'done' == action.action:
            break
        elif 'give_up' == action.action:
            print('Stucked')
            print(a.KB0)
            for c in a.KB:
                print(c)
            break
    
    # Results
    print('====Result====')  
    b.print_current_board()
    print()
    print('====Answer====')
    b.print_answer_board()
    print('==============')
    if b.check_success():
        print('Success')
    else:
        print('Fail')
    
    search_time = (time.time() - start_time)
    print(search_time, 's')
