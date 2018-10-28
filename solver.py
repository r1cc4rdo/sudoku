from io import board_to_pretty, string_to_board


def propagate_out(board):
    """
    Remove a known value from other groups (row, col, square)
    """
    for rcs, values in board.iteritems():  # for all cells
        if len(values) == 1:  # if allocated
            for other_values in board.peers(rcs, values):  # for all peers
                other_values -= values  # remove cell value from other cell possible values


def propagate_in(board):
    """
    If all other values in a group cover all but 1 number, you're that number
    """
    for rcs, values in board.iteritems():
        for fun, index in zip((board.row, board.col, board.square), rcs):
            values_left = set(range(1, 10)) - set(value for values in fun(index, values) for value in values)
            if len(values_left) == 1:
                values = values_left


def twin_cells(board):
    """
    If two cells in a group share the same two possible values, remove those values from the rest of the group
    """
    for rcs, values in board.iteritems():
        if len(values) != 2:
            continue

        for fun, index in zip((board.row, board.col, board.square), rcs):
            for other_values in fun(index, values):
                if values == other_values:
                    for neither in fun(index, values):
                        if neither is not other_values:
                            neither -= values


def solve(board):

    print board_to_pretty(board)

    prev = 0
    while True:

        values = sum(len(values) for values in board.itervalues())
        if values == prev or values == 81:
            break

        propagate_out(board)
        propagate_in(board)
        twin_cells(board)

        prev = values

    print board_to_pretty(board, 9)
    return values


if __name__ == '__main__':

    board_string = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."
    solve(string_to_board(board_string))
