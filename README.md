![Sudoku solve animation](./images/solve.gif)

# A minimal Sudoku solver

What you will find here:

* a [minimal implementation of a Sudoku](https://github.com/r1cc4rdo/sudoku/blob/master/sudoku.py) solver
  (self-contained in 1 page of code).
* [Code](https://github.com/r1cc4rdo/sudoku/blob/master/sudoku/board_plot.py) to print beautiful boards such as
  the one shown above ;)
* An explanation of what I mean by minimal.

### A single logical rule to solve sudokus

This all started, like many things, on a whim. On a plane. By the time the flight was over, I had a [basic working
version of the code](https://github.com/r1cc4rdo/sudoku/blob/master/sudoku/solver_wo_search.py) that could solve all
the "hard" boards from the plane's entertainment system. Back under the coverage of WiFi, it became soon obvious that
Sudokus existed that my code could not solve: [searching for "hardest sudoku" on Google](https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html),
one typically lands on this Telegraph page for the infamous "Everest" board, from Arto Inkala.

![Stuck on the everest](./images/everest.png)

There are dozens of strategies for solving sudokus. [My original code](https://github.com/r1cc4rdo/sudoku/blob/master/sudoku/solver_wo_search.py)
only implemented three:

* _basic elimination_ (remove a known value from peers candidates)
* _sole candidate_ (if all peers in a group cover all but 1 number, you're that number)
* _naked twins_ (if two cells in a group share the same two candidate values, remove those values from peers)

but there are many more. Here are a few pages I found with collections of basic and advanced sudoku strategies:

1. [sudokuDragon.com basic strategies](http://www.sudokudragon.com/sudokustrategy.htm)
2. [sudokuDragon.com advanced strategies](http://www.sudokudragon.com/advancedstrategy.htm)
3. [kristanix.com solving techniques](https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php)
4. [sudokuWiki strategy families](http://www.sudokuwiki.org/Strategy_Families)

While coding the next obvious rule to add ["hidden twins"](http://www.sudokuwiki.org/Hidden_Candidates) it became
obvious to me that they were just instances of a more general rule that encompassed altogether _hidden twins_,
_naked twins_, hidden/naked triples, quadruples and so on.

Moreover, that _basic elimination_ and _sole candidate_ were also instances of that same rule, when the subset of
interest (a pair, a triple, etc.) were of size 1. Here's [code](https://github.com/r1cc4rdo/sudoku/blob/master/sudoku/solver_w_search.py) implementing that single general rule:

    for subset_size, group in product(range(1, 9), board.groups):
        for subset in combinations((cell for cell in group if len(board[cell]) == subset_size), subset_size):
            possible_values_in_subset = reduce(lambda s, cell: s | board[cell], subset, set())
            if len(possible_values_in_subset) == len(subset):  # we found a constraint
                all_supersets = [g for g in board.groups if all(cell in g for cell in subset)]
                for cell in [cell for g in all_supersets for cell in g if cell not in subset]:
                    board[cell] -= possible_values_in_subset

In words, it says: _"for every subset of N cells in any row, column or square; if there are only N candidate values in
the subset, you can remove those values from the cells' peers in any row, column or square that contains the subset"_.
The reasoning is similar to the ["hidden twins"](http://www.sudokuwiki.org/Hidden_Candidates) case: we do not know
where values are going to be allocated within the subset, but know that they cannot appear elsewhere in the cells'
peers for any group they are part of.

The _basic elimination_ strategy corresponds to a subset size of 1: we have a cell, it contains 1 candidate value, so
we can remove it from every row, colums of square that cell belongs to. _sole candidate_ corresponds to a subset size of
8: there are 8 cells, covering up 8 values so the single cell left out must take the 9th one. Similarly, _naked twins_
corresponds to a subset of size 2, and its dual _hidden twins_ to a subset of size 6.

Overall, those 7 lines of code cover the following (using name from [sudokuDragon.com](http://www.sudokudragon.com/sudokustrategy.htm)):

* _basic elimination_ (subset size: 1)
* _sole candidate_ (subset size: 8)
* _unique candidate_ (subset size: 8)
* _only square_ (subset size: 8)
* _two out of three_ (subset size: 8)
* _sub-group exclusion_
* _naked twins_ (subset size: 2)
* _hidden twins_ (subset size: 6)
* _naked triplets_ (subset size: 3)
* _hidden triplets_ (subset size: 5)
* _general permutation_
* _naked chains_
* _hidden chains_



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

Old:

Note: twin, triples and propagate out are instances of a more general rule we'll call divide_and_conquer.
If you can divide a group in two sets of m and n elements (n + m == 9) and the subset of size n only contains
instances of n distinct values, then you can remove those values from the elements of m. This subsumes propagate
out because a single element containing a value is then erases than element from the groups it belongs.

After you divide into two group, the elimination step applies to every group all cells belong to.

#### References:
4. http://norvig.com/sudoku.html
5. https://en.wikipedia.org/wiki/Mathematics_of_Sudoku
6. https://en.wikipedia.org/wiki/Sudoku_solving_algorithms


http://www.sudokuwiki.org/sudoku.htm?bd=800000000003600000070090200050007000000045700000100030001000068008500010090000400

1. http://www.sudokudragon.com/sudokustrategy.htm
2. http://www.sudokudragon.com/advancedstrategy.htm
3. https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
4. http://www.sudokuwiki.org/Strategy_Families

https://github.com/r1cc4rdo/sudoku

http://norvig.com/sudoku.html
