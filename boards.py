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

board_strings = {
  "simple":   ".276..5.8.9..1...26.4.82...27.9.......17.54.......8.91...29.1.55...7..8.3.2..467.",
  "hard1":    "7.4..591.1...6..8....17.3.5.....8.91..34.96..68.7.....4.6.81....7..9...4.953..1.2",
  "hard2":    "5....3...791..6..3.....15.78..3....2.6.....8.1....2..53.76.....9..2..751...4....6",
  "hard3":    ".2..9..34...2...181....3.....8.4..9.75.....46.1..5.7.....9....159...6...38..1..7.",
  "hard4":    ".2...9..5.963...12.........4...97.2...82.49...3.15...4.........68...174.1..9...6.",
  "harder":   "...91....8.25....1.7.2...4......8.2..4.1....8..5.2...4........9..6......427.6....",
  "harder2":  "...6..2..8.4.3.........9...4.5.....771.........3.5...83...7...4.....19.....2...6.",
  "harder3":  "..36.49......5....9.......72.......6.4.....5.8.......11.......5..........9273641.",
  "everest":  "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."}


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
    can be fed back to representation_to_board
    """
    width = max(filter(lambda value: value <= multi_values, (len(cell['values']) for cell in board)))
    values = [''.join(str(value) for value in cell['values']) for cell in board]
    values = [(value if len(value) <= width else '.').center(width) for value in values]

    representation = ''
    horizontal_line = '+'.join(['-' * (1 + (width + 1) * 3)] * 3) + '\n'
    for value, cell in zip(values, board):

        if cell['col'] == 0:
            representation += ' '

        representation += value + ' '

        if cell['col'] in (2, 5):
            representation += '| '

        if cell['col'] == 8:
            representation += '\n'

        if cell['row'] in (2, 5) and cell['col'] == 8:
            representation += horizontal_line

    return representation


def board_to_string(board):
    """
    Prints a one-liner version of a board, displaying all unambiguously allocated numbers or a '.' otherwise.
    Example: ".276..5.8.9..1...26.4.82...27.9.......17.54.......8.91...29.1.55...7..8.3.2..467."
    """
    strings = [''.join(map(str, cell['values'])) for cell in board]
    return ''.join(s if len(s) == 1 else '.' for s in strings)


def representation_to_board(board_representation):
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

    or 800000000003600000070090200050007000000045700000100030001000068008500010090000400
    or 8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..

    and return the internal representation for a sudoku board (a collection of 81 sets,
    containing the possible values for a cell).
    """
    board = []
    blanks = '.x0'
    char_counter = 0
    for character in board_representation:

        if not (character.isdigit() or character in blanks):
            continue

        col = char_counter % 9
        row = char_counter // 9
        square = 3 * (row / 3) + col / 3
        values = set((int(character),) if character not in blanks else range(1, 10))
        board.append({'row': row, 'col': col, 'square': square, 'values': values})

        char_counter += 1

    return board


if __name__ == '__main__':

    for name, board_string in board_strings.iteritems():
        print '{}\n'.format(name)
        print board_to_pretty(representation_to_board(board_string))
