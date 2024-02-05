# =============================
# Student Names: Hunter Coker, Brandon Liang, Udo Ojeh
# Group ID: Group 22
# Date: February 2nd, 2024
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc: Provides three unique CSP implementations that take a valid Cagey grid as an input and returns a csp and a list of variables.

#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *

from itertools import product

from itertools import permutations

def binary_ne_grid(cagey_grid):
    n = cagey_grid[0]  # Gets the grid size N from the input Cagey Grid

    # Creates variables representing each cell in the grid with a domain from 1 to n
    variables = [Variable(f"Cell({i+1},{j+1})", list(range(1, n+1))) for i in range(n) for j in range(n)]
    constraints = []

    # Rows: Binary not-equal constraints
    for i in range(1, n+1):
        for j in range(1, n):
            for k in range(j + 1, n + 1):
                # Create a binary not-equal constraint for each pair of cells in the same row
                constraint = Constraint(f"Row_NE_{i}_{j}_{k}", [variables[(i-1)*n + j - 1], variables[(i-1)*n + k - 1]])
                constraint.add_satisfying_tuples([(x, y) for x in range(1, n+1) for y in range(1, n+1) if x != y])
                constraints.append(constraint)

    # Columns: Binary not-equal constraints
    for i in range(1, n+1):
        for j in range(1, n):
            for k in range(j + 1, n + 1):
                # Create a binary not-equal constraint for each pair of cells in the same column
                constraint = Constraint(f"Col_NE_{i}_{j}_{k}", [variables[(j-1)*n + i - 1], variables[(k-1)*n + i - 1]])
                constraint.add_satisfying_tuples([(x, y) for x in range(1, n+1) for y in range(1, n+1) if x != y])
                constraints.append(constraint)

    # Creates a CSP with a name and the list of variables
    csp = CSP("binary_ne_grid", variables)

    # Adds all of the constraints to the newly created CSP
    for constraint in constraints:
        csp.add_constraint(constraint)

    return csp, variables

def nary_ad_grid(cagey_grid):
    n = cagey_grid[0] # Gets the grid size N from the input Cagey Grid

    # Creates variables representing each cell in the grid with a domain from 1 to n
    variables = [Variable(f"Cell({i+1},{j+1})", list(range(1, n+1))) for i in range(n) for j in range(n)]
    constraints = []

    # Rows: N-ary all-different constraints
    for i in range(1, n+1):     
        # 1. Gets all the variables in the same row
        variables_in_row = [variables[(i-1)*n + j] for j in range(n)]

        # 2. Creates an N-ary constraint for that row
        constraint = Constraint(f"Row_{i}", variables_in_row)

        # 3. Add satisfying tuples for the constraint (In this case, all permutations of values from 1 to n)
        constraint.add_satisfying_tuples([tuple(row) for row in permutations(range(1, n+1))])

        # 4. Add the constraint to the list of constraints
        constraints.append(constraint)

    # Columns: N-ary all-different constraints 
    for i in range(1, n+1):

        # 1. Gets all the variables in the same column
        variables_in_column = [variables[(j-1)*n + i - 1] for j in range(1, n+1)]

        # 2. Creates an N-ary constraint for that column
        constraint = Constraint(f"Col_{i}", variables_in_column)

        # 3. Add satisfying tuples for the constraint (In this case, all permutations of values from 1 to n)
        constraint.add_satisfying_tuples([tuple(column) for column in permutations(range(1, n+1))])

        # 4. Add the constraint to the list of constraints
        constraints.append(constraint)

    # Creates a CSP with a name and the list of variables
    csp = CSP("nary_ad_grid", variables)

    # Adds all of the constraints to the newly created CSP
    for constraint in constraints:
        csp.add_constraint(constraint)

    return csp, variables

def cagey_csp_model(cagey_grid):
    
    csp, variables = nary_ad_grid(cagey_grid)
    n = cagey_grid[0] # Gets the grid size N from the input Cagey Grid
    constraints = csp.get_all_cons()

    # Cage constraints
    operand_variables = []

    for cage in cagey_grid[1]:
        v = cage[0]
        indices = cage[1]
        op = cage[2]
        
        var_names = [f"Var-Cell({i},{j})" for (i, j) in indices]
        cage_variables = [variables[(i-1)*n + j - 1] for i, j in indices]

        operand_variable = Variable(f"Cage_op({v}:{op}:[{', '.join(var_names)}])", ["+", "-", "*", "/"])
        operand_variables.append(operand_variable)

        # Generating Satisfying Tuples
        
        # Generate all possible combinations of values for the cage variables
        satisfying_tuples = []
        variable_values = [range(1, n + 1) for _ in indices]
        variable_combinations = product(*variable_values)

        # Check each combination and add to satisfying tuples if it satisfies the cage constraint
        for values in variable_combinations:

            # Apply the specified operation to the values
            if op == '+':
                result = sum(values)
            elif op == '-':
                result = values[0] - sum(values[1:])
            elif op == '*':
                result = 1
                for value in values:
                    result *= value
            elif op == '/':
                if all(value % values[0] == 0 for value in values[1:]):
                    result = values[1] // values[0]
            elif op == '?':
                # Unknown operation: return any result
                result = sum(values)
            if result == v:
                satisfying_tuple = (op,) + values
                satisfying_tuples.append(satisfying_tuple)

        # Creates a cage constraint and adds the satisfying tuples for the constraint
        constraint = Constraint(f"Cage_{v}_{op}", [operand_variable] + cage_variables)
        constraint.add_satisfying_tuples(satisfying_tuples)

        # Adds the cnew constraint to the list of all constraints
        constraints.append(constraint)

    # Adds the operand variables to the list of alll variables (variables from the created grid)
    variables += operand_variables 

    # Creates a CSP with a name and the list of variables
    csp = CSP("cagey_csp_model", variables)

    # Adds all of the constraints to the newly created CSP
    for constraint in constraints:
        csp.add_constraint(constraint)

    return csp, variables
