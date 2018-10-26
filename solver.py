from boards import *


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


def solve(board):

    print board_to_representation(board)

    prev = 0
    while True:

        values = sum(len(cell['values']) for cell in board)
        if values == prev or values == 81:
            break

        propagate_out(board)
        propagate_in(board)
        twin_cells(board)

        prev = values

    print board_to_representation(board, 9)


if __name__ == '__main__':

    name = 'hard1'

    print '\n' + name + '\n'
    solve(representation_to_board(boards[name]))
