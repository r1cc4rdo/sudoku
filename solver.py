def propagate_out(board):
    """
    Remove a known value from other groups (row, col, square)
    """
    for cell in board:
        if len(cell['values']) == 1:
            for other_cell in board:
                if cell is not other_cell and any([cell[group] == other_cell[group] for group in ('row', 'col', 'square')]):
                    other_cell['values'] -= cell['values']


def propagate_in(board):
    """
    If all other values in a group cover all but 1 number, you're that number
    """
    for cell in board:
        groups = []
        for group in ('row', 'col', 'square'):

            group_values = []
            for other_cell in board:
                if cell is not other_cell and any([cell[group] == other_cell[group]]):
                    group_values.append(other_cell['values'])

            groups.append(set(range(1, 10)) - set(el for els in group_values for el in els))

        for values_in_group in groups:
            if len(values_in_group) == 1:
                cell['values'] = values_in_group


def twin_cells(board):
    """
    If two cells in a group share the same two possible values, remove those values from the rest of the group
    """
    for group in ('row', 'col', 'square'):
        for num in range(10):
            cells = [cell for cell in board if cell[group] == num]
            for cell in cells:
                if len(cell['values']) != 2:
                    continue
                for other_cell in cells:
                    if cell is other_cell:
                        continue
                    if cell['values'] == other_cell['values']:
                        for group_cell in cells:
                            if group_cell is cell or group_cell is other_cell:
                                continue
                            group_cell['values'] -= cell['values']


def pretty_print(board):
    print ''
    desc = ''.join(str(tuple(cell['values'])[0]) if len(cell['values']) == 1 else ' ' for cell in board)
    for line in range(9):
        print desc[9*line+0:9*line+3], '|', desc[9*line+3:9*line+6], '|', desc[9*line+6:9*line+9]
        if line == 2 or line == 5:
            print '----+-----+----'


def solve(board):

    pretty_print(board)

    prev = 0
    while True:

        values = sum(len(cell['values']) for cell in board)
        if values == prev or values == 81:
            break

        propagate_out(board)
        propagate_in(board)
        twin_cells(board)

        prev = values

    pretty_print(board)


def input_to_board(board_strings):

    board = []
    for row, nums in enumerate(board_strings):
        for col, num in enumerate(nums):

            square = 3 * (row / 3) + col / 3
            values = set((int(num),) if num != ' ' else range(1, 10))
            board.append({'row': row, 'col': col, 'square': square, 'values': values})

    return board


if __name__ == '__main__':

    boards = {
        "simple": (' 276  5 8',
                   ' 9  1   2',
                   '6 4 82   ',
                   '27 9     ',
                   '  17 54  ',
                   '     8 91',
                   '   29 1 5',
                   '5   7  8 ',
                   '3 2  467 '),

        "hard1": ('7 4  591 ',
                  '1   6  8 ',
                  '   17 3 5',
                  '     8 91',
                  '  34 96  ',
                  '68 7     ',
                  '4 6 81   ',
                  ' 7  9   4',
                  ' 953  1 2'),

        "hard2": ('5    3   ',
                  '791  6  3',
                  '     15 7',
                  '8  3    2',
                  ' 6     8 ',
                  '1    2  5',
                  '3 76     ',
                  '9  2  751',
                  '   4    6'),

        "hard3": (' 2  9  34',
                  '   2   18',
                  '1    3   ',
                  '  8 4  9 ',
                  '75     46',
                  ' 1  5 7  ',
                  '   9    1',
                  '59   6   ',
                  '38  1  7 '),

        "hard4": (' 2   9  5',
                  ' 963   12',
                  '         ',
                  '4   97 2 ',
                  '  82 49  ',
                  ' 3 15   4',
                  '         ',
                  '68   174 ',
                  '1  9   6 '),

        "denali": ('   91    ',
                   '8 25    1',
                   ' 7 2   4 ',
                   '     8 2 ',
                   ' 4 1    8',
                   '  5 2   4',
                   '        9',
                   '  6      ',
                   '427 6    '),

        "everest": ('8        ',
                    '  36     ',
                    ' 7  9 2  ',
                    ' 5   7   ',
                    '    457  ',
                    '   1   3 ',
                    '  1    68',
                    '  85   1 ',
                    ' 9    4  '),

        "template": ('',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '')
    }

    solve(input_to_board(boards['hard4']))
