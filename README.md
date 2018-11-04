![Sudoku solve animation](./images/solve.gif)
# A minimal Sudoku solver

What you will find here:

* a [minimal implementation of a Sudoku][1] solver (self-contained in 1 page of code).
* [Code][2] to print beautiful boards such as the one shown above ;)
* A rambling explanation of what I mean by "minimal".

### A single logical rule to solve sudokus

This all started, like many things, on a whim. On a plane. By the time the flight was over, I had a [basic working
version of the code][3] that could solve all the "hard" boards from the plane's entertainment system. Back under the
coverage of WiFi, it became soon obvious that Sudokus existed that my code could not solve: [searching for "hardest
sudoku" on Google][4], one typically lands on [this Telegraph page][5] for the infamous "Everest" board, from Arto
Inkala.
![Stuck on the everest](./images/everest.png)

There are dozens of strategies for solving sudokus. [My original code][3] only implements three:

* _basic elimination_ (remove a known value from peers' candidates)
* _sole candidate_ (if all peers in a group cover all but 1 number, you're that number)
* _naked twins_ (if two cells in a group share the same two candidate values, remove those values from peers)

but there are many more. Here are a few pages I found with collections of basic and advanced sudoku strategies:

1. [sudokuDragon.com basic strategies][6]
2. [sudokuDragon.com advanced strategies][7]
3. [kristanix.com solving techniques][8]
4. [sudokuWiki strategy families][9]

While coding the next obvious rule to add ["hidden twins"][10] it became
obvious to me that they were just instances of a more general rule that encompassed altogether _hidden twins_,
_naked twins_, hidden/naked triples, quadruples and so on.

Moreover, that _basic elimination_ and _sole candidate_ were also instances of that same rule, when the subset of
interest (a pair, a triple, etc.) were of size 1. Here's [code][11] implementing that single general rule:

    for subset_size, group in product(range(1, 9), board.groups):
        for subset in combinations((cell for cell in group if len(board[cell]) == subset_size), subset_size):
            possible_values_in_subset = reduce(lambda s, cell: s | board[cell], subset, set())
            if len(possible_values_in_subset) == len(subset):  # we found a constraint
                all_supersets = [g for g in board.groups if all(cell in g for cell in subset)]
                for cell in [cell for g in all_supersets for cell in g if cell not in subset]:
                    board[cell] -= possible_values_in_subset

In words, it says: _"for every subset of N cells in any row, column or square; if there are only N candidate values in
the subset, you can remove those values from the cells' peers in any row, column or square that contains the subset"_.
The reasoning is similar to the ["hidden twins"][10] case: we do not know
where values are going to be allocated within the subset, but know that they cannot appear elsewhere in the cells'
peers for any group they are part of.

The _basic elimination_ strategy corresponds to a subset size of 1: we have a cell, it contains 1 candidate value, so
we can remove it from every row, colums of square that cell belongs to. _sole candidate_ corresponds to a subset size
of 8: there are 8 cells, covering up 8 values so the single cell left out must take the 9th one. Similarly,
_naked twins_ corresponds to a subset of size 2, and its dual _hidden twins_ to a subset of size 6.

Overall, those 7 lines of code cover the following (using name from [sudokuDragon.com][6]):

* _basic elimination_ (subset size: 1)
* _sole candidate_ (subset size: 8)
* _unique candidate_ (subset size: 8)
* _only square_ (subset size: 8)
* _two out of three_ (subset size: 8)
* _sub-group exclusion_ (iterated elimination)
* _pointing pairs_ (common supersets)
* _pointing triples_ (common supersets)
* _naked twins_ (subset size: 2)
* _hidden twins_ (subset size: 6)
* _naked triplets_ (subset size: 3)
* _hidden triplets_ (subset size: 5)
* _general permutation_
* _naked chains_
* _hidden chains_

So, _this is awesome_. This single rule suffices to solve most sudokus rated "very hard", "super fiendish", and
equivalent. But it is sufficient to solve any and every sudoku board?
![Stuck on the everest](./images/everest_marked.png)

The answer is "no".

Since it operates on a single group at a time, and propagates information within groups only if they
share cells, it fails to capture the group to group dependencies exploited by [more advanced strategies][7].
So surely, if we were to implement all of them, we would them be able to solve every sudoku, right?

The answer is again, sadly, "no".

One easy way to convince oneself is to open the [Everest board on SudokuWiki.com solver][12].
There, you can click repeatedly on the "Take step" button, which will apply a large collection of strategies to the
board and still ultimately fail to recover the solution.

Let's have a second look at the Everest board shown above. The red numbers are those participating in a [_"conjugated
pair"_][7] that it is what most advanced strategies concentrate on. You
can generate your own visualization of partially completed board with the [_plot\_board_][2]

The red numbers are

you can generate with

advanced strategies focus on creating chains of

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











[1]: https://github.com/r1cc4rdo/sudoku/blob/master/sudoku.py  "Self-contained solver"
[2]: https://github.com/r1cc4rdo/sudoku/blob/master/sudoku/board_plot.py "Graphical sudoku plot"
[3]: https://github.com/r1cc4rdo/sudoku/blob/master/sudoku/solver_wo_search.py "Basic solver w/o search"
[4]: http://lmgtfy.com/?q=hardest+sudoku "Search for \"hardest sudoku\" on Google"
[5]: https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html "Everest board from Arto Inkala"

[6]: http://www.sudokudragon.com/sudokustrategy.htm "sudokuDragon.com basic strategies"
[7]: http://www.sudokudragon.com/advancedstrategy.htm "sudokuDragon.com advanced strategies"
[8]: https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php "kristanix.com solving techniques"
[9]: http://www.sudokuwiki.org/Strategy_Families "sudokuWiki strategy families"

[10]: http://www.sudokuwiki.org/Hidden_Candidates "Hidden candidates strategy"
[11]: https://github.com/r1cc4rdo/sudoku/blob/master/sudoku/solver_w_search.py "Solver with single rule and search"
[12]: http://www.sudokuwiki.org/sudoku.htm?bd=800000000003600000070090200050007000000045700000100030001000068008500010090000400 "Everest board in SudokuWiki's solver"

[]: http://norvig.com/sudoku.html "Peter Norvig's sudoku solver"

[] https://en.wikipedia.org/wiki/Mathematics_of_Sudoku "Wikipedia: Mathematics of Sudoku"
[] https://en.wikipedia.org/wiki/Sudoku_solving_algorithms "Wikipedia: Sudoku solving algorithms"
