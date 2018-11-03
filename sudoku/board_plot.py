import matplotlib.patches as patches
import matplotlib.pyplot as plot
from collections import Counter

from solver_w_search import eliminate_plus, search


def plot_board(board, always_print_pencil_marks=False, colorize_conjugated_pairs=False):
    """
    Plots a beautiful sudoku board using matplotlib.
    """
    plot.figure().add_subplot(111, aspect='equal')
    plot.axis('off')

    for origin in ((0.3, 0.0), (0.0, 0.3), (0.6, 0.3), (0.3, 0.6)):
        rect = patches.Rectangle(origin, 0.3, 0.3, facecolor=(0.96,) * 3)
        plot.gca().add_patch(rect)

    for step in range(10):  # print grid
        plot.plot((0.1 * step, 0.1 * step), (0, 0.9), 'k-', linewidth=4 if step % 3 == 0 else 1)
        plot.plot((0, 0.9), (0.1 * step, 0.1 * step), 'k-', linewidth=4 if step % 3 == 0 else 1)

    for (r, c, s), possible_values in board.iteritems():  # print numbers
        centered = {'horizontalalignment': 'center', 'verticalalignment': 'center'}
        bx, by = 0.048 + 0.1 * c, 0.048 + 0.1 * (8 - r)
        if len(possible_values) == 1:  # assigned cells

            plot.text(bx, by, str(list(possible_values)[0]), fontsize=25, **centered)

        elif len(possible_values) < 9 or always_print_pencil_marks:  # pencil marks

            conjugated = []
            if colorize_conjugated_pairs:
                groups = [[rcs for rcs in board if rcs[rcs_type] == num] for num in range(9) for rcs_type in range(3)]
                for group in [group for group in groups if (r, c, s) in group]:
                    counter = Counter([value for rcs in group for value in board[rcs] if len(board[rcs]) > 1])
                    conjugated.extend(element for element, count in counter.iteritems() if count == 2)

            for value in possible_values:
                dx, dy = (value - 1) % 3 - 1, 1 - (value - 1) // 3
                plot.text(bx + 0.028 * dx, by + 0.028 * dy, str(value), fontsize=10,
                          color='red' if value in conjugated else (0.2,) * 3, **centered)


def plot_solve(board):

    allocated = prev = 1 + 9**3
    group_subset_dim = 1
    while allocated > 81:

        plot_board(board)

        allocated = sum(len(candidates) for candidates in board.itervalues())
        if allocated == prev and group_subset_dim == 4:
            return search(board)

        group_subset_dim = 1 if allocated < prev else group_subset_dim + 1
        eliminate_plus(board, group_subset_dim)
        prev = allocated

    return board
