from board import Board
from logic import Literal, Clause, CNF
from agent import Agent

if __name__ == '__main__':
    b = Board('easy')
    a = Agent()

    b.print_board()

    for pos in b.init_safe_pos:
        new_clause = Clause( [-Literal(pos)] )
        if new_clause not in a.KB:
            a.KB.append(new_clause)
            
    while True:
        query_pos = a.take_action(b)
        new_hint = b.query(query_pos)
        if new_hint == -3:
            print('Fail on', query_pos)
            break
        a.new_hint(query_pos, new_hint, b)
        b.print_current_board()
        print()