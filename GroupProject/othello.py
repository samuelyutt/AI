from board import Board
from agent import Agent, RandomAgent, GreedyAgent, DullAgent, Human
from MCTS import MCTSAgent


class Player():
    def __init__(self, agent, side = 0):
        self.agent = agent
        self.side = side
        self.name = 'Black' if side == 1 else 'White'

    def __str__(self):
        return str(self.agent) + ' (' + self.name + ')'


class Othello():
    def __init__(self, agent_Black, agent_White, print_mode = False):
        self.player_Black = Player(agent_Black, 1)
        self.player_White = Player(agent_White, -1)
        self.board = Board()
        self.rounds = 0
        self.player_Black.agent.side = 1
        self.player_White.agent.side = -1
        self.print_mode = print_mode

    def take_turns(self):
        if self.rounds % 2 == 0:
            player = self.player_Black
        else:
            player = self.player_White
        self.rounds += 1
        return player

    def apply_action(self, player, action):
        if self.print_mode:
            print(player, 'on', action)
        self.board.move(player.side, action)

    def terminate(self):
        black_count, white_count = self.board.statistics()
        is_terminated = self.board.is_over()
        result = black_count - white_count
        if is_terminated:
            if self.print_mode:
                print(self.player_Black, black_count)
                print(self.player_White, white_count)
            if result > 0:
                if self.print_mode:
                    print(self.player_Black, 'wins by', result)
                return self.player_Black.side
            elif result < 0:
                if self.print_mode:
                    print(self.player_White, 'wins by', -result)
                return self.player_White.side
            elif result == 0:
                if self.print_mode:
                    print('Tie')
                return 0
        else:
            if self.print_mode:
                print('Something is wrong')
            return None

    def play(self):
        stuck_count = 0
        while True:
            if self.print_mode:
                print(self.board)
            player = self.take_turns()
            movable = self.board.movable(player.side)
            if len(movable):
                if self.print_mode:
                    print(self.rounds, 'Playing:', player)
                action = player.agent.take_action(self.board, movable)
                self.apply_action(player, action)
                stuck_count = 0
            else:
                if self.print_mode:
                    print(self.rounds, 'No moves for', player)
                stuck_count += 1
            if stuck_count == 2:
                winner = self.terminate()
                return winner


if __name__ == '__main__':
    agent1 = MCTSAgent(500)
    # agent1 = GreedyAgent()
    agent2 = Human()
    # agent1 = MCTSAgent(1000, type_=1)
    # agent1 = RandomAgent()
    # agent2 = MCTSAgent(900, type_=2)
    # agent2 = Human()

    game = Othello(agent1, agent2, print_mode = True)
    game.play()
    # game = Othello(agent1, agent2, print_mode = True)
    # game.play()

