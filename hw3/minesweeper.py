from board import Board, Action
from logic import Literal, Clause
from agent import Agent
import time
if __name__ == '__main__':
    b = Board('medium')
    a = Agent()

    for pos in b.init_safe_pos:
        new_clause = Clause( [-Literal(pos)] )
        a.add_clause_to_KB(new_clause)
    start_time = time.time()
    while True:
        b.print_current_board()
        print()
        # time.sleep(0.7)

        action = a.take_action(b)
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
            for c in a.KB:
                print(c)
            print(a.KB0)
            break
    
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
