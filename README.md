# A minimal Sudoku solver

What you will find here:

* a minimal implementation of a Sudoku solver (self-contained in 1 page of code)
* Code to print beautiful boards such as the one shown above ;)
* An explanation of what I mean by minimal.

https://github.com/r1cc4rdo/sudoku
http://norvig.com/sudoku.html


# Write up

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



# TODO

Code more rules:

    def another_rule(board):
        """
        If within a short row/col in a square, a number appears that does not exist in the rest of values of the square,
        eliminate from the rest of the long row/col
        """

or otherwise, code a uber rule:

    def triples(board):
        """
        Same thing with twin cells, but for three cells/values
        Note: twin, triples and propagate out are instances of a more general rule we'll call divide_and_conquer.
        If you can divide a group in two sets of m and n elements (n + m == 9) and the subset of size n only contains
        instances of n distinct values, then you can remove those values from the elements of m. This subsumes propagate
        out because a single element containing a value is then erases than element from the groups it belongs.
    
        After you divide into two group, the elimination step applies to every group all cells belong to.
        """
        pass
