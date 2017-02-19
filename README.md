# Sudoku Solver

Sudoku solver is an agent that solves any diagonal sudoku puzzle.

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: When we find two cells in the same unit (row,column, 3X3 squares or diagonals) such that they have identical values and length =2,
a contraint is found which is that no other cells in that unit can have either of those digits and thus we can use that to eliminate those digits from other cells of that unit.
We apply this constraint repeatedly (contraint propogation) until no identical cells of length 2 (Naked twins) are left in the grid.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The sudoku grid has 2 diagonals so we add the lists [A1, B2 ... I9] and [A9, B8, ... I1)] to the unitlists and apply the following constraints on it repeatedly:
1. eliminate : For every unit(row,column, 3X3 squares or diagonals), we make sure that no cell contains the digits present in already solved cells (length == 1)
2. Naked_Twins: We apply the naked twins constraint explained above
3. only_choice: in every unit, we make sure that if any cell contains a digits taht no other cell has, then we can solve that cell by giving it the value of that digit.

### Running and Visualizing the solution

To visualize your solution, please navigate to the root folder and excecute the ```solution.py``` file
