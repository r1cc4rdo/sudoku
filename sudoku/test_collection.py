import os

from solver_w_search import solve
from board_io import string_to_board, board_to_pretty


def collection(filename):
    with open(os.path.join('collections', filename), 'r') as fin:
        while True:
            board_string = fin.readline()
            if not board_string:
                break

            yield string_to_board(board_string)


if __name__ == '__main__':

    count = total = 0
    for board in collection('test_db.txt'):

        print '-' * 30, '\n'
        print board_to_pretty(board)
        solved = solve(board)
        print board_to_pretty(solved, 9)

        count += 81 == sum(len(candidates) for candidates in solved.itervalues())
        total += 1

    print 'Solved: {} / {}'.format(count, total)
