# A self-contained sudoku solver. Find me here: https://github.com/r1cc4rdo/sudoku

from itertools import *

sudoku = """

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
groups = tuple([] for _ in range(27))
for index, (row, col) in enumerate(product(range(9), repeat=2)):
    for displacement, rcs in enumerate((row, col, 3 * (row / 3) + col / 3)):
        groups[rcs + displacement * 9].append(index)


def eliminate_candidates(board, groups=groups):
    for subset_size, group in product(range(1, 9), groups):
        for subset in combinations((index for index in group if len(board[index]) == subset_size), subset_size):
            possible_values_in_subset = reduce(lambda s, index: s | set(board[index]), subset, set())
            if len(possible_values_in_subset) == len(subset):  # we found a constraint
                all_supersets = [g for g in groups if all(index in g for index in subset)]
                for index in [index for g in all_supersets for index in g if index not in subset]:
                    board[index] = ''.join(value for value in board[index] if value not in possible_values_in_subset)
                    assert board[index]  # if triggered, inconsistent assignment detected


def solve(board):
    allocated, prev = 1 + 9**3, 2 + 9**3
    while 81 < allocated < prev:  # keep eliminating
        prev, allocated = allocated, sum(map(len, board))
        eliminate_candidates(board)
    if allocated == 81:  # we're done!
        return board
    lengths = map(len, board)  # otherwise, we need to search
    pivot = lengths.index(min(filter(lambda x: x > 1, lengths)))
    for board[pivot] in board[pivot]:
        try:
            return solve(board[:])
        except AssertionError as e:
            pass  # try next element
    raise AssertionError('No solutions found')  # keep searching in caller


if __name__ == '__main__':
    board = list(islice([c if c.isdigit() else '123456789' for c in sudoku if c.isdigit() or c in '.0'], 81))
    line, div = ' {} {} {} | {} {} {} | {} {} {} \n', '-------+-------+-------\n'
    print (line * 3 + div + line * 3 + div + line * 3).format(*solve(board))
