from minesweeper import MineSweeper, Result

def simple_test(rounds, difficulty, show = False):
    success = 0
    fail = 0
    stuck = 0
    success_duration = 0
    
    for i in range(rounds):
        game = MineSweeper(difficulty)
        result = game.play(show)
        if result.status == 'Success':
            success += 1
            success_duration += result.play_time
        elif result.status == 'Fail':
            fail += 1
        if result.stuck:
            stuck += 1

    print()
    print('==============')
    print('Tested:\t\t\t', rounds, difficulty, 'games')
    print('Success:\t\t', success, 'games')
    print('Success duration:\t', success_duration/rounds, 'sec per game')
    print('Fail (Stuck):\t\t {} ({}) games'.format(fail, stuck))


if __name__ == '__main__':
    simple_test(1000, 'easy')
    simple_test(1000, 'medium')
    simple_test(1000, 'hard')