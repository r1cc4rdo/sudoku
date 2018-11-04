![Sudoku solve animation](./images/solve.gif)
# A minimal Sudoku solver

What you will find here:

* a [minimal implementation of a Sudoku][1] solver (self-contained in 1 page of code).
* [Code][2] to print beautiful boards such as the one shown above ;)
* A rambling explanation of what I mean by "minimal".

## How many strategies are required to solve sudokus?

This all started, like many things, on a whim. On a plane. By the time the flight was over, I had a [basic working
version of the code][3] that could solve all the "hard" boards from the plane's entertainment system. Back under the
coverage of WiFi, I found Sudokus that my code could not solve: [searching for "hardest sudoku" on Google][4],
one typically lands on [this Telegraph page][5] for the infamous "Everest" board, from Arto Inkala.

!["Everest" sudoku board](./images/everest.png)

[My original code][3] only implements three strategies:

* _basic elimination_ (remove a known value from peers' candidates)
* _sole candidate_ (if all peers in a group cover all but 1 number, you're that number)
* _naked twins_ (if two cells in a group share the same two candidate values, remove those values from peers)

but there are dozens of them for solving sudokus. See for example:

1. [sudokuDragon.com basic strategies][6]
2. [sudokuDragon.com advanced strategies][7]
3. [kristanix.com solving techniques][8]
4. [sudokuWiki strategy families][9]

## A single, generic elimination strategy 

While coding the most promising new strategy to add, the ["hidden twins"][10] rule, it became obvious to me that it
was an instance of a more general rule (which we will call, for the rest of this piece, _the Rule_) that encompassed
altogether _hidden twins_, _naked twins_, hidden/naked triples, quadruples and so on. Moreover, that _basic
elimination_ and _sole candidate_ were also instances of that same rule, when the subset of interest (a pair, a triple,
etc.) were of size 1. Here's [code][11] implementing that single general strategy:

    for subset_size, group in product(range(1, 9), board.groups):
        for subset in combinations((cell for cell in group if len(board[cell]) == subset_size), subset_size):
            possible_values_in_subset = reduce(lambda s, cell: s | board[cell], subset, set())
            if len(possible_values_in_subset) == len(subset):  # we found a constraint
                all_supersets = [g for g in board.groups if all(cell in g for cell in subset)]
                for cell in [cell for g in all_supersets for cell in g if cell not in subset]:
                    board[cell] -= possible_values_in_subset

In words:

> for every subset of N cells in any row, column or square; if there are only N candidate values in the subset,
> you can remove those values from the cells' peers in any row, column or square that contains the subset.

The reasoning is similar to the ["naked twins"][10] rule: let's say we found two cells on the same row that can only
contain a 2 or a 4: we do not know which goes where, but know that these two values cannot appear elsewhere in the
cells' peers in that row and for any group the two cells are part of.

The _basic elimination_ strategy corresponds to a subset size of 1: we have a cell, it contains 1 candidate value, so
we can remove it from every row, colums of square that cell belongs to. _sole candidate_ corresponds to a subset size
of 8: there are 8 cells, covering up 8 values so the single cell left out must take the 9th one. _naked twins_
corresponds to a subset of size 2, its dual _hidden twins_ to a subset of size 6.

This strategy alone, in 7 lines of code, extends all the following (using terminology from [sudokuDragon.com][6]):

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

So, **this is awesome**. This single rule suffices to solve most sudokus rated "very hard", "super fiendish", and
equivalent. But is it enough to solve any and every sudoku board?

## Can the _Rule_ solve every sudoku board alone?

Let's look again at the Everest board shown above. After iteratively applying the _Rule_, the following state is what
we are left with. The small numbers in each square not filled are the potential remaining candidates for that cell
(the "pencil marks"). The red ones are those participating in a [_"conjugated pair"_][7], more on that later (you can
generate your own visualizations of partially completed board with the [_plot\_board_][2] function; see the
[notebook][13] for an example).

![Stuck on the everest](./images/everest_marked.png)

So, the answer is "no".

The _Rule_ is not enought by itself. Since it operates on a single group at a time, and propagates information within
groups only if they share cells, it fails to capture the group to group dependencies exploited by [more advanced
strategies][7]. Were we to implement those too, would we be capable of solving every sudoku?

The answer is again, sadly, "no".

One easy way to convince oneself is to open the [Everest board on SudokuWiki.com solver][12]. There, you can click
repeatedly on the "Take step" button, which applies a large collection of advanced strategies to the board and still
ultimately fail to recover the solution.

## Is search/backtracking necessary?

All the [advanced strategies][7] such as X-Wing, Swordfish, X-Y-Wing and extensions all look for either an even or odd
number of chained conjugate pairs (pairs of cells that, for a candidate number, mutually exclude each other). In the
even case, these rules search for candidates that are eliminated by either alternate allocation of values on the chain.
In the odd case, one allocation causes an inconsistency and can be eliminated.

All these strategies consider two or more alternate allocation of values and analyze the state of the board in either
case. They are _search and backtracking_ strategies in disguise, no more clever than brute forcing through all possible
combinations. 

Since all the strategies based on conjugated tuples are equivalent to _search and backtracking_, the latter is the
second and final strategy required for solving any sudoku board. You can find the relevant code in [solver_w_search.py][11]
and a self-contained implementation in a single file in [sudoku.py][1].

[Peter Norvig's implementation][14] justifies the introduction of search to avoid the tedious exercise of implementing
dozens of rules. Turns out adding it is a necessary evil if we are to solve any possible sudoku instance. 

Ultimately the question "can every sudoku instance be solved logically?" is debatable. On one hand, there exist sudoku
boards that human-applicable rules cannot crack. On the other, the _search and backtracking_ strategy often considered
inelegant is an instance of [proof by contradiction][17], which is indeed part of the logic arsenal.

Refer to Wikipedia to read more about [the mathematics of sudoku][15] and the availble [solving algorithms][16].

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
[13]: https://github.com/r1cc4rdo/sudoku/blob/master/sudoku.ipynb "Sudoku solver notebook"
[14]: http://norvig.com/sudoku.html "Peter Norvig's sudoku solver"
[15]: https://en.wikipedia.org/wiki/Mathematics_of_Sudoku "Wikipedia: Mathematics of Sudoku"
[16]: https://en.wikipedia.org/wiki/Sudoku_solving_algorithms "Wikipedia: Sudoku solving algorithms"
[17]: https://en.wikipedia.org/wiki/Proof_by_contradiction "Wikipedia: proof by contradiction"
