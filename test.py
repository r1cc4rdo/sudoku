from collections import OrderedDict

from solver import solve
from sudoku_io import string_to_board


board_strings = OrderedDict((
  ("simple",  ".276..5.8.9..1...26.4.82...27.9.......17.54.......8.91...29.1.55...7..8.3.2..467."),
  ("hard1",   "7.4..591.1...6..8....17.3.5.....8.91..34.96..68.7.....4.6.81....7..9...4.953..1.2"),
  ("hard2",   "5....3...791..6..3.....15.78..3....2.6.....8.1....2..53.76.....9..2..751...4....6"),
  ("hard3",   ".2..9..34...2...181....3.....8.4..9.75.....46.1..5.7.....9....159...6...38..1..7."),
  ("hard4",   ".2...9..5.963...12.........4...97.2...82.49...3.15...4.........68...174.1..9...6."),
  ("harder",  "...91....8.25....1.7.2...4......8.2..4.1....8..5.2...4........9..6......427.6...."),
  ("harder2", "...6..2..8.4.3.........9...4.5.....771.........3.5...83...7...4.....19.....2...6."),
  ("harder3", "..36.49......5....9.......72.......6.4.....5.8.......11.......5..........9273641."),
  ("everest", "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..")))


if __name__ == '__main__':

    count = 0
    detail_count = 0
    for name, board_string in board_strings.iteritems():

        print '-' * 5, name, '-' * 35, '\n'
        candidates = solve(string_to_board(board_string))
        print '{}: {}\n'.format(name, 'OK' if candidates == 81 else "NO")
        detail_count += candidates - 81
        count += candidates == 81

    print '\nSolved: {} / {} (score: {}, lower is better)'.format(count, len(board_strings), detail_count)

# TODO: 6 vs 4 / 9 from old to new code
