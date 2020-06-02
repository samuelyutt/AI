from board import Board
from agent import Agent, RandomAgent, GreedyAgent, Human


class Player():
    def __init__(self, agent, side = 0):
        self.agent = agent
        self.side = side
        self.name = 'Black' if side == 1 else 'White'

    def __str__(self):
        return str(self.agent) + ' (' + self.name + ')'


class Othello():
    def __init__(self, agent_Black, agent_White):
        self.player_Black = Player(agent_Black, 1)
        self.player_White = Player(agent_White, -1)
        self.board = Board()
        self.rounds = 0
        self.player_Black.agent.side = 1
        self.player_White.agent.side = -1

    def take_turns(self):
        if self.rounds % 2 == 0:
            player = self.player_Black
        else:
            player = self.player_White
        self.rounds += 1
        return player

    def apply_action(self, player, action):
        print(player, 'on', action)
        self.board.move(player.side, action)

    def terminate(self):
        black_count, white_count, is_terminated = self.board.statistics()
        result = black_count - white_count
        if is_terminated:
            print(self.player_Black, black_count)
            print(self.player_White, white_count)
            if result > 0:
                print(self.player_Black, 'wins by', result)
                return self.player_Black
            elif result < 0:
                print(self.player_White, 'wins by', -result)
                return self.player_White
            elif result == 0:
                print('Tie')
                return None
        else:
            print('Something is wrong')
            return None

    def play(self):
        stuck_count = 0
        while True:
            print(self.board)
            player = self.take_turns()
            movable = self.board.movable(player.side)
            if len(movable):
                print(self.rounds, 'Playing:', player)
                action = player.agent.take_action(self.board, movable)
                self.apply_action(player, action)
                stuck_count = 0
            else:
                print(self.rounds, 'No move for', player)
                stuck_count += 1
            if stuck_count == 2:
                winner = self.terminate()
                break;


if __name__ == '__main__':
    agent1 = RandomAgent()
    agent2 = GreedyAgent()

    game = Othello(agent1, agent2)
    game.play()