from othello import Othello
from agent import Agent, RandomAgent, GreedyAgent, DullAgent, Human
from MCTS import MCTSAgent


if __name__ == '__main__':
    agent1 = MCTSAgent(1000)
    agents = [RandomAgent(), GreedyAgent(), DullAgent(), MCTSAgent(200)]

    for agent2 in agents:
        print('========')
        print(agent1, 'vs', agent2)
        black_win = 0
        white_win = 0
        tie = 0
        for _ in range(100):
            game = Othello(agent1, agent2, print_mode = False)
            winner = game.play()
            if winner == 1:
                black_win += 1
            elif winner == -1:
                white_win += 1
            elif winner == 0:
                tie += 1
        print(agent1, black_win)
        print(agent2, white_win)
        print('Tie', tie)
        print()
