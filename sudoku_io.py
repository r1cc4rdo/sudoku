from collections import OrderedDict
from itertools import islice


def board_to_pretty(board, multi_values=1):
    """
    Pretty prints a board.
    Given the following state of computation, obtained with board_to_representation(board, 9):

        8      1246   24569  |   2347   12357    1234  |  13569    4579  1345679
      12459    124      3    |    6     12578    1248  |   1589   45789   14579
       1456     7      456   |   348      9      1348  |    2      458    13456
    -------------------------+-------------------------+-------------------------
      123469    5      2469  |   2389    2368     7    |   1689    2489   12469
      12369   12368    269   |   2389     4       5    |    7      289     1269
      24679    2468   24679  |    1      268     2689  |   5689     3     24569
    -------------------------+-------------------------+-------------------------
      23457    234      1    |  23479    237     2349  |   359      6       8
      23467    2346     8    |    5      2367   23469  |    39      1      2379
      23567     9      2567  |   2378   123678  12368  |    4      257     2357

    board_to_representation(board, 3) is:

      8   .   .  |  .   .   .  |  .   .   .
      .  124  3  |  6   .   .  |  .   .   .
      .   7  456 | 348  9   .  |  2  458  .
    -------------+-------------+-------------
      .   5   .  |  .   .   7  |  .   .   .
      .   .  269 |  .   4   5  |  7  289  .
      .   .   .  |  1  268  .  |  .   3   .
    -------------+-------------+-------------
      .  234  1  |  .  237  .  | 359  6   8
      .   .   8  |  5   .   .  |  39  1   .
      .   9   .  |  .   .   .  |  4  257  .

    and board_to_representation(board)

     8 . . | . . . | . . .
     . . 3 | 6 . . | . . .
     . 7 . | . 9 . | 2 . .
    -------+-------+-------
     . 5 . | . . 7 | . . .
     . . . | . 4 5 | 7 . .
     . . . | 1 . . | . 3 .
    -------+-------+-------
     . . 1 | . . . | . 6 8
     . . 8 | 5 . . | . 1 .
     . 9 . | . . . | 4 . .

    This last representation, equivalent to the defaults multi_values=1,
    and can be fed back to representation_to_board(...)
    """
    value_strings = [''.join(str(value) for value in values) for values in board.itervalues()]
    value_strings = [value if len(value) <= multi_values else '.' for value in value_strings]
    width = max(len(value_string) for value_string in value_strings)

    sl = ' {} {} {} | {} {} {} | {} {} {} \n'  # standard line
    hd = '+'.join(['-' * (1 + (width + 1) * 3)] * 3) + '\n'  # horizontal divider
    return (sl * 3 + hd + sl * 3 + hd + sl * 3).format(*(value_string.center(width) for value_string in value_strings))


def board_to_string(board):
    """
    Prints a one-liner version of a board, displaying all unambiguously allocated numbers or a '.' otherwise.
    Example: ".276..5.8.9..1...26.4.82...27.9.......17.54.......8.91...29.1.55...7..8.3.2..467."
    """
    strings = [''.join(map(str, values)) for values in board.itervalues()]
    return ''.join(s if len(s) == 1 else '.' for s in strings)


def string_to_board(board_representation):
    """
    Accepts inputs such as:

     8 . . | . . . | . . .
     . . 3 | 6 . . | . . .
     . 7 . | . 9 . | 2 . .
    -------+-------+-------
     . 5 . | . . 7 | . . .
     . . . | . 4 5 | 7 . .
     . . . | 1 . . | . 3 .
    -------+-------+-------
     . . 1 | . . . | . 6 8
     . . 8 | 5 . . | . 1 .
     . 9 . | . . . | 4 . .

    or 800000000003600000070090200050007000000045700000100030001000068008500010090000400 comment, or name
    or 8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.. anything after is ignored

    and return the internal representation for a sudoku board (a collection of 81 sets,
    containing the possible values for a cell, indexed by (row, col, square)).
    """
    blanks = '.x0'
    board = OrderedDict()
    for cnt, c in enumerate(islice([c for c in board_representation if c.isdigit() or c in blanks], 81)):
        row, col, values = cnt // 9, cnt % 9, {int(c),} if c not in blanks else range(1, 10)
        board[(row, col, 3 * (row / 3) + col / 3)] = values
    return board


if __name__ == '__main__':

    board_string = "..36.49......5....9.......72.......6.4.....5.8.......11.......5..........9273641."

    board = string_to_board(board_string)
    print '\nInternal representation:\n'
    for k, v in board.iteritems():
        print k, ': ', v

    print '\nto_string:\n\n', board_to_string(board)
    print '\npretty\n\n', board_to_pretty(board)

    template = """ . . . | . . . | . . . 
                   . . . | . . . | . . . 
                   . . . | . . . | . . . 
                  -------+-------+-------
                   . . . | . . . | . . . 
                   . . . | . . . | . . . 
                   . . . | . . . | . . . 
                  -------+-------+-------
                   . . . | . . . | . . . 
                   . . . | . . . | . . . 
                   . . . | . . . | . . . 
    """
    print board_to_string(string_to_board(template))
