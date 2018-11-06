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
for index, (r, c) in enumerate(product(range(9), repeat=2)):
    for rcs, displacement in zip((r, c, 3 * (r / 3) + c / 3), range(0, 27, 9)):
        groups[rcs + displacement].append(index)


def eliminate_candidates(board, groups=groups):
    for subset_size, group in product(range(1, 9), groups):
        for subset in combinations((index for index in group if len(board[index]) == subset_size), subset_size):
            possible_values_in_subset = reduce(lambda s, index: s | set(board[index]), subset, set())
            if len(possible_values_in_subset) == len(subset):  # we found a constraint
                all_supersets = [g for g in groups if all(index in g for index in subset)]
                for index in [index for g in all_supersets for index in g if index not in subset]:
                    board[index] = ''.join(value for value in board[index] if value not in possible_values_in_subset)
                    assert board[index]


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
    raise AssertionError('Search failed')


def string_to_board(board_string, blanks='.0'):
    return list(islice([c if c.isdigit() else '123456789' for c in board_string if c.isdigit() or c in blanks], 81))


def board_to_pretty(board):
    width = max(map(len, board))
    sl = ' {} {} {} | {} {} {} | {} {} {} \n'  # standard line
    hd = '+'.join(['-' * (1 + (width + 1) * 3)] * 3) + '\n'  # horizontal divider
    return (sl * 3 + hd + sl * 3 + hd + sl * 3).format(*(values.center(width) for values in board))


if __name__ == '__main__':
    print board_to_pretty(solve(string_to_board(sudoku)))
