from sudoku_io import board_to_pretty, string_to_board


def eliminate(board):
    """
    Remove a known value from other groups (row, col, square)
    """
    for rcs, values in board.iteritems():
        if len(values) == 1:  # cell is allocated
            for other_rcs, other_values in board.iteritems():
                if any(group == other_group for group, other_group in zip(rcs, other_rcs)) and rcs != other_rcs:
                    other_values -= values  # remove cell value from other cell possible values
                    assert other_values


def unique_candidate(board):
    """
    If all other values in a group cover all but 1 number, you're that number
    """
    groups = [[rcs for rcs in board if rcs[rcs_type] == num] for num in range(9) for rcs_type in range(3)]
    for rcs, values in board.iteritems():
        for group in [group for group in groups if rcs in group]:
            group_peers = [other_rcs for other_rcs in group if rcs != other_rcs]
            values_covered = set(value for other_rcs in group_peers for value in board[other_rcs])
            if len(values_covered) == 8:
                values -= values_covered
                assert values


def naked_twins(board):
    """
    If two cells in a group share the same two possible values, remove those values from the rest of the group
    """
    groups = [[rcs for rcs in board if rcs[rcs_type] == num] for num in range(9) for rcs_type in range(3)]
    for rcs, values in board.iteritems():
        if len(values) != 2:
            continue

        for group in [group for group in groups if rcs in group]:
            group_peers = [other_rcs for other_rcs in group if rcs != other_rcs]
            for other_rcs in group_peers:
                if values == board[other_rcs]:
                    for neither in [neither for neither in group_peers if other_rcs != neither]:
                        board[neither] -= values
                        assert board[neither]


def solve_three_rules(board):

    print board_to_pretty(board)

    prev = 0
    while True:

        values = sum(len(values) for values in board.itervalues())
        if values == prev or values == 81:
            break

        eliminate(board)
        unique_candidate(board)
        naked_twins(board)

        prev = values

    print board_to_pretty(board, 9)
    return values


if __name__ == '__main__':

    board_string = ".2..9..34...2...181....3.....8.4..9.75.....46.1..5.7.....9....159...6...38..1..7."
    board = string_to_board(board_string)
    solve_three_rules(board)
