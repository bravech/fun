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

def solve():
    # All the variables we need: each cell has one of the 9 digits
    lits = []
    diags = [[0, 1, 1, 1, 56], [0, 3, 1, 1, 18], [5, 0, -1, 1, 45], [2, 8, 1, -1, 25], [6, 8, 1, -1, 8], [8, 2, -1, -1, 11], [8, 5, -1, -1, 24]] 

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
    # cage_lits = {}
    # for cage in cages:
    #     cage_lits[cage[0]] = []
    
    
    # for i in range(9):
    #     for j in range(9):
    #         if cage_grid[i][j] != '0':
    #             cage_lits[cage_grid[i][j]].append((i, j))
    # print(cage_lits)


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

    # Constraint #4: Diagonal Sums

    diag_lits = []
    print(diags)
    for d in diags:
        x, y, a, b, p = d
        temp = []
        for i in range(9):
            if x + a * i  >= 0 and x + a * i <= 8 and y + i * b >= 0 and y + i * b <= 8:
                temp.append(lits[x + a * i][y + b * i])
        print(temp, p)
        clauses.append(Sum(temp) == p)
    

    # Constraint #5: Squares are even

    squares = [[3, 0], [7, 0], [1, 2], [5, 2], [3, 4], [7, 4], [1, 6], [5, 6]]
    circles = [[2, 1], [6, 1], [0, 3], [4, 3], [8, 3], [2, 5], [6, 5], [0, 7], [4, 7]]

    for a,b in circles:
        l = lits[a][b]
        clauses.append(Or([l==2, l==4, l==6, l==8]))
    
    for a,b in squares:
        l = lits[a][b]
        clauses.append(Or([l==1, l==3, l==5, l==7, l==9]))

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
    solve()


