from z3 import *
from itertools import combinations
import json


def sum_1_thru_9(literals, n):
    clauses = []
    for i, j in combinations(range(9), 2):
        clauses.append(If(And([literals[i] == 1, literals[j] == 9]), Sum(literals[i+1:j]) == n, True))
    for j, i in combinations(range(9), 2):
        clauses.append(If(And([literals[i] == 1, literals[j] == 9]), Sum(literals[j+1:i]) == n, True))
    return clauses

# def exactly_one(literals):
#     clauses = [literals]        # at least one of the literals is true
#     # Now encode no more than one literal is true.
#     # Hint: there is no pair of literals such that both are true.
#     for comb in combinations(literals, 2):
#         clauses += [[Not(comb[0]), Not(comb[1])]]
#     return clauses

def exactly_one(literals):
    sums = []
    for i in range(9):
        sums.append(Sum([If(l == i+1, 1, 0) for l in literals]))
    # print(sums)
    clauses = [s == 1 for s in sums]
    return clauses

def solve(cage_grid, cages):
    # All the variables we need: each cell has one of the 9 digits
    lits = []
    nums = [[1, 3, 5, 2, 4, 7, 9, 6, 8], [7, 9, 2, 6, 8, 3, 5, 1, 4], [4, 6, 8, 1, 5, 9, 3, 7, 2], [6, 2, 4, 9, 7, 1, 8, 3, 5], [3, 8, 1, 5, 2, 4, 6, 9, 7], [9, 5, 7, 3, 6, 8, 2, 4, 1], [5, 7, 3, 8, 1, 6, 4, 2, 9], [8, 1, 6, 4, 9, 2, 7, 5, 3], [2, 4, 9, 7, 3, 5, 1, 8, 6]]

    for i in range(9):
        line = []
        for j in range(9):
            line.append(Int("x_%i_%i" % (i, j)))
        lits.append(line)
    
    # for i in range(9):
    #     line = []
    #     for j in range(9):
    #         line.append(IntVal(nums[i][j]))
    #     lits.append(line)

    clauses = []
    cage_lits = {}
    for cage in cages:
        cage_lits[cage[0]] = []
    
    
    for i in range(9):
        for j in range(9):
            if cage_grid[i][j] != '0':
                cage_lits[cage_grid[i][j]].append((i, j))
    print(cage_lits)


    # Set of contraints #1: a cell is between 0 and 9.
    for i in range(9):
        for j in range(9):
            clauses.append(And([lits[i][j] >= 0, lits[i][j] <= 9]))
    

    # Set of constraints #2: each value is used only once in a row.
    # for j in range(9):
    #     for k in range(9):
    #         clauses += exactly_one([lits[i][j][k] for i in range(9)])
    for i in range(9):
        print(lits[i])
        clauses += exactly_one(lits[i])
    # print(exactly_one(lits[0]))

    # Set of constraints #3: each value used exactly once in each column:
    # for i in range(9):
    #     for k in range(9):
    #         clauses += exactly_one([lits[i][j][k] for j in range(9)])
    for j in range(9):
        clauses += exactly_one([lits[i][j] for i in range(9)])

    # Set of constraints #4: each value used exactly once in each 3x3 grid.

    for x in range(3):
        for y in range(3):
            grid_cells = []
            for a in range(3):
                for b in range(3):
                    grid_cells.append(lits[3 * x + a][3 * y + b])
            clauses += exactly_one(grid_cells)

    # Set of constraints #5: No UDLR neighbors can contain numerically adjacent digits (1 and 2, 4 and 5)

    rows = len(lits)
    cols = len(lits[0])
    for i in range(9):
        for j in range(9):
            for a, b in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
                if i + a >= 0 and i + a < rows and j + b >= 0 and j + b < cols:
                    clauses.append(And([lits[i][j] != lits[i+a][j+b] + 1, lits[i][j] != lits[i+a][j+b] - 1]))
    
    # Set of constraints #6: Clues outside puzzle show sum of digits sandwiched between 1 and 9 in that row or column
    for i in range(9):
        if row_sums[i] != 0:
            clauses += sum_1_thru_9(lits[i], row_sums[i])
    
    for j in range(9):
        if col_sums[j] != 0:
            clauses += sum_1_thru_9([lits[i][j] for i in range(9)], col_sums[j])

    # Set of constraints #7: cages sum to a number:
    for name, targ in cages:
        cs = cage_lits[name]
        clauses.append(Sum([lits[a][b] for (a, b) in cs]) == targ)
    
    # Set of constraints #8: cages have no duplicates
    # debugs = []
    # for name in cage_lits:
    #     cs = cage_lits[name]
    #     clauses += exactly_one([lits[a][b] for (a, b) in cs])
    
    # for i in range(len(debugs)):
    #     clauses += debugs[i]
    #     s = Solver()
    #     for clause in clauses:
    #         s.add(clause)
    #     if str(s.check()) == "unsat":
    #         print(i)
    #         break




    # # Encode the grid constraints
    # for i in range(9):
    #     for j in range(9):
    #         if grid[i][j] > 0:
    #             clauses += [[lits[i][j][grid[i][j] - 1]]]

    s = Solver()

    for clause in clauses:
        s.add(clause)
    print(s.check())

    if str(s.check()) == 'sat':
        print_solution(s.model(), lits)
    else:
        print("unsat")


def print_solution(m, lits):
    for i in range(9):
        out = ""
        for j in range(9):
            out += str(m[lits[i][j]])
        print(out)

if __name__ == "__main__":
    cage_grid = []
    cages = []
    row_sums = [21, 0, 0, 0, 0, 0, 0, 0, 0]
    col_sums = [20, 0, 0, 0, 0, 0, 35, 0, 0]
    with open("miracle_grid.txt") as input_grid:
        for i in range(9):
            cage_grid.append(list(input_grid.readline().strip()))
        for i in range(9):
            a, b = input_grid.readline().split()
            b = int(b)
            cages.append((a, b))
    print(cages)
    solve(cage_grid, cages)


