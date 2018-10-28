from io import board_to_pretty, string_to_board
from itertools import chain, combinations


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


def one_rule_to_rule_them_all(board):

    subsets_indexes = list(chain.from_iterable(combinations(range(9), num + 1) for num in range(8)))
    for group in [board.rows, board.cols, board.squares]:  # for every row, col and square
        for group_index in range(9):
            for subset_indexes in subsets_indexes:  # for every subset of the group

                subset = [group[group_index][index] for index in subset_indexes]
                subset_possible_values = reduce(lambda a, b: a.union(b), subset)
                if len(subset_possible_values) == len(subset):  # if the subset contains as many values as cells

                    # if here, we found a group of cells that cast a constraints on the remainder of any group they belong

                    # if len(subset_possible_values) < 4:
                    #
                    #     for other_group in rows, cols, squares:  # for any group the cells belong to
                    #         for other_group_index in range(9):
                    #             if all(cell in other_group[other_group_index] for cell in subset):
                    #
                    #                 for cell in other_group[other_group_index]:
                    #                     if cell in subset:
                    #                         continue
                    #
                    #                     cell -= subset_possible_values  # remove the other cells
                    #
                    # else:

                    other_indexes = [index for index in range(9) if index not in subset_indexes]
                    for other_index in other_indexes:
                        group[group_index][other_index] -= subset_possible_values  # remove the other cells


def solve(board):

    print board_to_pretty(board)

    prev = 0
    while True:

        values = sum(len(values) for values in board.itervalues())
        if values == prev or values == 81:
            break

        one_rule_to_rule_them_all(board)
        # propagate_out(board)
        # propagate_in(board)
        # twin_cells(board)

        prev = values

    print board_to_pretty(board, 9)
    return values


if __name__ == '__main__':

    board_string = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."
    board = string_to_board(board_string)
    solve(board)

    print board.rows
    print board.cols
    print board.squares
