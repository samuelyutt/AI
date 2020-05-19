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
    print('Success duration:\t', success_duration/success, 'sec per game')
    print('Fail (Stuck):\t\t {} ({}) games'.format(fail, stuck))

def mines_count_test(rounds, difficulty, mines, show = False):
    print('==============')
    print('Tested:', rounds, difficulty, 'games per mines_counts')
    print('Mines\tSuccess\tStuck\tFail\tFail-Stuck\tSuccess duration')
    for m in range(1, mines+1):
        success = 0
        fail = 0
        stuck = 0
        success_duration = 0

        for i in range(rounds):
            game = MineSweeper(difficulty, m)
            result = game.play(show)
            if result.status == 'Success':
                success += 1
                success_duration += result.play_time
            elif result.status == 'Fail':
                fail += 1
            if result.stuck:
                stuck += 1

        print('{}\t{}\t{}\t{}\t{}\t\t{}'.format(m, success, stuck, fail, fail-stuck, success_duration/success))


if __name__ == '__main__':
    simple_test(1000, 'easy')
    simple_test(1000, 'medium')
    simple_test(1000, 'hard')
    mines_count_test(100, 'medium', 40)
