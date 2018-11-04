"""
A self-contained sudoku solver.
This is just code from the sudoku module in a single file stripped of comments and blank lines.
For details on functions and parameters, look at board_io.py and solver_w_search.py
"""
from itertools import combinations, product, islice
from collections import OrderedDict
from copy import deepcopy


def eliminate(board):
    for subset_size, group in product(range(1, 9), board.groups):
        for subset in combinations((rcs for rcs in group if len(board[rcs]) == subset_size), subset_size):
            possible_values_in_subset = reduce(lambda s, k: s | board[k], subset, set())
            if len(possible_values_in_subset) == len(subset):  # we found a constraint
                all_supersets = [g for g in board.groups if all(rcs in g for rcs in subset)]
                for rcs in [rcs for g in all_supersets for rcs in g if rcs not in subset]:
                    board[rcs] -= possible_values_in_subset
                    assert board[rcs]


def search(board):
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
        eliminate(board)
    return board


def string_to_board(board_representation):
    blanks = '.x0'
    board = OrderedDict()
    for cnt, c in enumerate(islice([c for c in board_representation if c.isdigit() or c in blanks], 81)):
        row, col, values = cnt // 9, cnt % 9, set([int(c)] if c not in blanks else range(1, 10))
        board[(row, col, 3 * (row / 3) + col / 3)] = values
    board.groups = [[rcs for rcs in board if rcs[rcs_type] == num] for num in range(9) for rcs_type in range(3)]
    return board


def board_to_pretty(board, multi_values=1):
    value_strings = [''.join(str(value) for value in values) for values in board.itervalues()]
    value_strings = [value if len(value) <= multi_values else '.' for value in value_strings]
    width = max(len(value_string) for value_string in value_strings)
    sl = ' {} {} {} | {} {} {} | {} {} {} \n'  # standard line
    hd = '+'.join(['-' * (1 + (width + 1) * 3)] * 3) + '\n'  # horizontal divider
    return (sl * 3 + hd + sl * 3 + hd + sl * 3).format(*(value_string.center(width) for value_string in value_strings))


if __name__ == '__main__':
    board_string = """

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

    """
    print board_to_pretty(solve(string_to_board(board_string)))
