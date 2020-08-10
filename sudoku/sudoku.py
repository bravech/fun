from z3 import *
from itertools import combinations


def exactly_one(literals):
    clauses = [literals]        # at least one of the literals is true
    # Now encode no more than one literal is true.
    # Hint: there is no pair of literals such that both are true.
    for comb in combinations(literals, 2):
        clauses += [[Not(comb[0]), Not(comb[1])]]
    return clauses


def print_solution(model, lits):
    grid = []
    for i in range(9):
        grid.append([])
        for j in range(9):
            color = 0
            for k in range(9):
                if model.evaluate(lits[i][j][k]):
                    color = k + 1
            grid[i].append(color)

    for line in grid:
        print(" ".join([str(x) for x in line]))


def solve(grid):
    # All the variables we need: each cell has one of the 9 digits
    lits = []
    for i in range(9):
        line = []
        for j in range(9):
            column = []
            for k in range(9):
                column.append(Bool("x_%i_%i_%i" % (i, j, k)))
            line.append(column)
        lits.append(line)

    clauses = []

    # Set of contraints #1: a cell has only one value.
    for i in range(9):
        for j in range(9):
            clauses += exactly_one(lits[i][j])

    # Set of constraints #2: each value is used only once in a row.
    for j in range(9):
        for k in range(9):
            clauses += exactly_one([lits[i][j][k] for i in range(9)])

    # Set of constraints #3: each value used exactly once in each column:
    for i in range(9):
        for k in range(9):
            clauses += exactly_one([lits[i][j][k] for j in range(9)])

    # Set of constraints #4: each value used exaclty once in each 3x3 grid.

    for x in range(3):
        for y in range(3):
            for k in range(9):
                grid_cells = []
                for a in range(3):
                    for b in range(3):
                        grid_cells.append(lits[3 * x + a][3 * y + b][k])
                clauses += exactly_one(grid_cells)

    # Encode the grid constraints
    for i in range(9):
        for j in range(9):
            if grid[i][j] > 0:
                clauses += [[lits[i][j][grid[i][j] - 1]]]

    s = Solver()

    for clause in clauses:
        s.add(Or(clause))

    if str(s.check()) == 'sat':
        print_solution(s.model(), lits)
    else:
        print("unsat")

# ================================================================================
#  You do not need to modify anything below this line.
# ================================================================================

def well_formed_problem(grid):
    for line in grid:
        if len(line) != 9:
            print("One line has the wrong number of columns.")
            return False
        for cell in line:
            if cell < 0 or cell > 9:
                print("One cell is not in range 0-9.")
                return False
    return (len(grid) == 9)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python sudoku.py INPUT_FILE\n\tHint: test_input contains two valid input files.")
        exit(1)

    _grid = []
    with open(sys.argv[1], 'r') as input_grid:
        # Each line is a line of the sudoku grid. We should have 9 lines of length 9
        for line in input_grid.readlines():
            _grid.append([int(x) for x in line.split(" ")])

        if well_formed_problem(_grid):
            # Call the encoding function on the input.
            solve(_grid)
            exit(0)
        else:
            print("The input file is invalid.")
            print("It should have 9 lines.")
            print("Each line with 9 digits  (number between 0-9) separated by spaces.")
            exit(1)
