from board_io import board_to_pretty, string_to_board
from itertools import combinations, product
from copy import deepcopy


def eliminate_plus(board, subset_size=1):
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
    groups = [[rcs for rcs in board if rcs[rcs_type] == num] for num in range(9) for rcs_type in range(3)]
    for subset_indexes, group in product(combinations(range(9), subset_size), groups):
        for group_subset in [[group[i] for i in range(9) if (i in subset_indexes) == tf] for tf in (True, False)]:
            possible_values_in_subset = reduce(lambda s, k: s | board[k], group_subset, set())
            if len(possible_values_in_subset) == len(group_subset):  # we found a constraint
                all_supersets = [group for group in groups if set(group_subset).issubset(set(group))]
                for rcs in [rcs for group in all_supersets for rcs in group if rcs not in group_subset]:
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

    allocated = prev = 1 + 9**3
    group_subset_dim = 1
    while allocated > 81:

        allocated = sum(len(candidates) for candidates in board.itervalues())
        if allocated == prev and group_subset_dim == 4:
            return search(board)

        group_subset_dim = 1 if allocated < prev else group_subset_dim + 1
        eliminate_plus(board, group_subset_dim)
        prev = allocated

    return board


if __name__ == '__main__':

    board_string = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."
    board = string_to_board(board_string)

    print board_to_pretty(board)
    board = solve(board)
    print board_to_pretty(board, 9)
