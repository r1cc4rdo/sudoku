from sudoku_io import board_to_pretty, string_to_board
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


def non_empty_proper_subsets(dim):
    """
    Return all the non-empty proper subset of a collection of size dim, as an iterator returning list of indexes.
    """
    return chain.from_iterable(combinations(range(dim), num) for num in range(1, dim))


def one_rule_to_rule_them_all(board):

    subsets_indexes = list(non_empty_proper_subsets(9))
    for group in chain.from_iterable((board.rows, board.cols, board.squares)):  # for every row, col and square
        for subset_indexes in subsets_indexes:  # for every subset of the group

            group_subset = [group[index] for index in subset_indexes]
            possible_values_in_subset = reduce(lambda s, rcs: s | board[rcs], group_subset, set())
            if len(possible_values_in_subset) == len(group_subset):  # if the subset contains as many values as cells, it's a constraint

                for other_group in chain.from_iterable((board.rows, board.cols, board.squares)):  # for any group the subset belongs to
                    if set(group_subset).issubset(set(other_group)):
                        for rcs in other_group:
                            if rcs not in group_subset:
                                board[rcs] -= possible_values_in_subset  # remove the other cells

                                assert(board[rcs])


def one_rule_to_rule_them_all_mod(board):
    """
    more ideas:
    https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    http://www.sudokudragon.com/sudokustrategy.htm
    http://www.sudokudragon.com/advancedstrategy.htm
    """
    subsets_indexes = list(non_empty_proper_subsets(9))
    for group in chain.from_iterable((board.rows, board.cols, board.squares)):  # for every row, col and square
        for subset_indexes in subsets_indexes:  # for every subset of the group

            group_subset = [group[index] for index in subset_indexes]
            possible_values_in_subset = reduce(lambda s, rcs: s | board[rcs], group_subset, set())

            # hidden subset - n numbers can only appear in n cells, erase other candidates from those cells

            remainder = [group[index] for index in range(9) if index not in subset_indexes]
            possible_values_in_remainder = reduce(lambda s, rcs: s | board[rcs], remainder, set())
            values_only_here = possible_values_in_subset - possible_values_in_remainder
            if len(values_only_here) == len(group_subset):
                for rcs in group_subset:
                    board[rcs] -= set(range(1, 9)) - values_only_here  # subtract not to overwrite set pointer

            # naked subset - n cells contains only n candidates, erase candidates from group remainder

            if len(possible_values_in_subset) == len(group_subset):  # if the subset contains as many values as cells, it's a constraint
                for other_group in chain.from_iterable((board.rows, board.cols, board.squares)):  # for any group the subset belongs to
                    if set(group_subset).issubset(set(other_group)):
                        for rcs in other_group:
                            if rcs not in group_subset:
                                board[rcs] -= possible_values_in_subset  # remove the other cells

                                assert(board[rcs])


def solve(board):

    print board_to_pretty(board)

    prev = 0
    while True:

        values = sum(len(values) for values in board.itervalues())
        if values == prev or values == 81:
            break

        one_rule_to_rule_them_all_mod(board)
        # propagate_out(board)
        # propagate_in(board)
        # twin_cells(board)

        prev = values

    print board_to_pretty(board, 9)
    if values > 81:
        print board_to_pretty(board)

    return values


if __name__ == '__main__':

    board_string = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."
    board = string_to_board(board_string)
    solve(board)

    print board.rows
    print board.cols
    print board.squares
