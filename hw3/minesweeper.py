import time
from board import Board, Action
from logic import Literal, Clause
from agent import Agent


class Result():
    def __init__(self, status, stuck, play_time):
        self.status = status
        self.stuck = stuck
        self.play_time = play_time


class MineSweeper():
    def __init__(self, difficulty, mines = None):
        self.board = Board(difficulty, mines)
        self.agent = Agent()
        self.debug = False

    def play(self, debug = None):
        if debug is not None:
            self.debug = debug
        start_time = time.time()
        stucked = False
        status = ''

        # Initial game
        for pos in self.board.init_safe_pos:
            new_clause = Clause( [-Literal(pos)] )
            self.agent.add_clause_to_KB(new_clause)
        
        while True:
            # Print current board
            if self.debug:
                self.board.print_current_board()
                print()

            # Take action
            action = self.agent.take_action(self.board)
            
            # Game flow
            if 'query' == action.action:
                new_hint = self.board.query(action.position)
                if new_hint == -3:
                    if self.debug:
                        print('Fail on', action.position)
                        break
                self.agent.new_hint(action.position, new_hint, self.board)
            elif 'mark_mine' == action.action:
                self.board.mark_mine(action.position)
            elif 'done' == action.action:
                break
            elif 'give_up' == action.action:
                stucked = True
                if self.debug:
                    print(self.agent.KB0)
                    for c in self.agent.KB:
                        print(c)
                    print('Stucked')
                break
        

        # Statistics
        play_time = (time.time() - start_time)
        if self.board.check_success():
            status = 'Success'
        else:
            status = 'Fail'

        if self.debug:
            # Results
            print('====Result====')  
            self.board.print_current_board()
            print()
            print('====Answer====')
            self.board.print_answer_board()
            print('====Status====')            
            print(status)
            print('Duration:', play_time, 'sec')

        return Result(status, stucked, play_time)

if __name__ == '__main__':
    # Examples
    game = MineSweeper('easy')
    game.play(debug = True)
