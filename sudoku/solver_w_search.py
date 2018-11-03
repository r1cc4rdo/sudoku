from board_io import board_to_pretty, string_to_board
from itertools import combinations, product
from copy import deepcopy


def eliminate_plus(board):
    """
    This rule subsumes several weaker rules for solving Sudokus.
    Other than the basic elimination strategy that removes a known cell value from the possible candidates for peers,
    it also applies the strategies "sole candidate", "unique candidate", "only square", "two out of three", "sub-group
    exclusion", "hidden twins", "naked twins", "hidden triplets", "naked triplets" and in general when iterated it is a
    generic substitute for "general permutation", "naked chains", and "hidden chains".

    This suffices to solve most sudokus rated "very hard", "super fiendish", and equivalent.
    Since this operates on a single group at a time, and propagates information within groups only if they
    share cells, it cannot solve all sudokus by itself. All the other advanced strategies for solving extremely
    hard sudokus are based on graph-coloring and hypothesis testing.
    """
    for subset_size, group in product(range(1, 9), board.groups):
        for subset in combinations((rcs for rcs in group if len(board[rcs]) == subset_size), subset_size):
            possible_values_in_subset = reduce(lambda s, k: s | board[k], subset, set())
            if len(possible_values_in_subset) == len(subset):  # we found a constraint
                all_supersets = [g for g in board.groups if all(rcs in g for rcs in subset)]
                for rcs in [rcs for g in all_supersets for rcs in g if rcs not in subset]:
                    board[rcs] -= possible_values_in_subset
                    assert board[rcs]


def search(board):
    """
    Takes the cell with the least number of candidates and tries all of them.
    Eventually, one allocation will succeed.
    """
    lengths = [len(values) for values in board.values()]
    pivot = board.keys()[lengths.index(min(filter(lambda x: x > 1, lengths)))]
    for element in board[pivot]:
        board_copy = deepcopy(board)
        board_copy[pivot] = {element}
        try:
            return solve(board_copy)
        except AssertionError as e:
            pass  # try next element
    raise AssertionError('Search failed')


def solve(board):

    allocated = 1 + 9**3
    while allocated > 81:

        prev, allocated = allocated, sum(len(candidates) for candidates in board.itervalues())
        if allocated == prev:  # no progress
            return search(board)

        eliminate_plus(board)

    return board


if __name__ == '__main__':

    board_string = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."
    board = string_to_board(board_string)

    print board_to_pretty(board)
    board = solve(board)
    print board_to_pretty(board, 9)
