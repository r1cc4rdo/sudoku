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
