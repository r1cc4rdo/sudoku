from itertools import combinations, product
from collections import OrderedDict
from copy import deepcopy


def one_rule_to_rule_them_all(board, subset_size=1):
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
            propagate(board_copy)
            return board_copy
        except AssertionError as e:
            pass


def propagate(board):
    prev_candidates = 0
    subset_size = 1
    while True:

        candidates_count = sum(len(candidates) for candidates in board.itervalues())
        if candidates_count == 81:  # we're done
            break

        if candidates_count == prev_candidates:  # no progress
            if subset_size == 4:  # we used all our smart rules already
                return search(board)
            else:  # use smarter rules
                subset_size += 1
        else:  # progress, reset subset size
            subset_size = 1

        one_rule_to_rule_them_all(board, subset_size)
        prev_candidates = candidates_count

    return board


def string_to_board(board_representation):
    blanks = '.x0'
    char_counter = 0
    board = OrderedDict()
    for character in board_representation:
        if character.isdigit() or character in blanks:
            row, col = char_counter // 9, char_counter % 9
            values = set((int(character),) if character not in blanks else range(1, 10))
            board[(row, col, 3 * (row / 3) + col / 3)] = values
            char_counter += 1

    return board


def board_to_string(board):
    strings = [''.join(map(str, values)) for values in board.itervalues()]
    return ''.join(s if len(s) == 1 else '.' for s in strings)


if __name__ == '__main__':
    board_string = "...6..2..8.4.3.........9...4.5.....771.........3.5...83...7...4.....19.....2...6."
    board = string_to_board(board_string)
    print board_to_string(propagate(board))
