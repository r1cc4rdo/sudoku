from board_plot import plot_board
from board_io import board_to_pretty, string_to_board
from itertools import combinations, product
from copy import deepcopy


def eliminate_plus(board, subset_size=1):
    """
    This rule subsumes several weaker rules for solving Sudokus.
    When subset_size == 1 and applied iteratively, it implements the basic elimination strategy that removes a known
    cell value from the possible candidates for peers. It also applies the "sole candidate", "unique candidate",
    "only square", "two out of three", and "sub-group exclusion" strategies (using the terminology of [1, 2]).
    When subset_size == 2, it is equivalent to applying the "hidden twins" rule (for subset of size 7), and the
    "naked twin" rule (for subsets of size 2). Equivalently, when subset_size == 3, implements "hidden triplets"
    (subset of size 6) and "naked triplet" (subset of size 3). In general, again using the terminology of [1, 2],
    when iterated it is a generic substitute for "general permutation", "naked chains", and "hidden chains".

    This suffices to solve most sudokus rated "very hard", "super fiendish", and equivalent.
    Since this operates on a single group at a time, and propagates information within groups only if they
    share cells, it cannot solve all sudokus by itself.

    All the advanced strategies for solving very hard sudokus are based on graph-coloring and hypothesis testing.
    X-Wing, Swordfish, X-Y-Wing and extensions all look for either an even or odd number of chained conjugate pairs
    (pairs of cells that, for a candidate number, mutually exclude each other). In the even case, rules search for
    candidates that are eliminated by either allocation of the chain. In the odd case, one allocation causes an
    inconsistency and can be eliminated.

    I see all these rules as instances of graph coloring / search / hypothesis testing -- no more clever than brute
    forcing through all possible combinations. Since there exists sudokus that cannot be solved without resorting
    to enumeration, and that require an elephantine or artificial memory to keep track of temporary allocation, I
    feel no remorse in implementing a search strategy into a solver. My reason, contrary to [4], is not that search
    avoids implementing a plethora of rules; on the contrary, after generalizing all rules I came across, this one
    rule and search are the only two distinct ones standing.

    References:
    [1] http://www.sudokudragon.com/sudokustrategy.htm
    [2] http://www.sudokudragon.com/advancedstrategy.htm
    [3] https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    [4] http://norvig.com/sudoku.html
    [5] https://en.wikipedia.org/wiki/Mathematics_of_Sudoku
    [6] https://en.wikipedia.org/wiki/Sudoku_solving_algorithms

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

    lengths = [len(values) for values in board.values()]
    pivot = board.keys()[lengths.index(min(filter(lambda x: x > 1, lengths)))]
    for element in board[pivot]:
        board_copy = deepcopy(board)
        board_copy[pivot] = {element}
        try:
            solve(board_copy)
            return board_copy
        except AssertionError as e:
            pass


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


def solve_debug(board, debug=False, plot=False):

    if plot:
        plot_board(board)
    else:
        print board_to_pretty(board)

    prev = 0
    depth = 1
    while True:

        values = sum(len(values) for values in board.itervalues())
        if values == 81:
            break

        if values == prev:
            if depth == 4:
                print 'I regrettably need to search'
                search(board)
            depth += 1
        else:
            depth = 1

        if debug:
            print 'Current score: {}, applying with depth == {}\n'.format(values, depth)

        eliminate_plus(board, depth)

        if debug:
            if plot:
                plot_board(board)
            else:
                print board_to_pretty(board, 9)

        prev = values

    if not debug:
        if plot:
            plot_board(board)
        else:
            print board_to_pretty(board, 9)
    return values


if __name__ == '__main__':

    # board_string = "...6..2..8.4.3.........9...4.5.....771.........3.5...83...7...4.....19.....2...6."
    board_string = ".2..9..34...2...181....3.....8.4..9.75.....46.1..5.7.....9....159...6...38..1..7."
    board = string_to_board(board_string)

    print board_to_pretty(board)
    solve(board)
    print board_to_pretty(board, 9)
