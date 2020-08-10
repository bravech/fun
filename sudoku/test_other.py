# Testing my logic in z3
from z3 import *
from itertools import combinations

def exactly_one(literals):
    sums = []
    for i in range(9):
        sums.append(Sum([If(l == i, 1, 0) for l in literals]))
    print(sums)
    clauses = [s == 1 for s in sums]
    return clauses

def sum_1_thru_9(literals, n):
    clauses = []
    for i, j in combinations(range(9), 2):
        clauses.append(If(And([literals[i] == 1, literals[j] == 9]), Sum(literals[i+1:j]) == n, True))
    for j, i in combinations(range(9), 2):
        clauses.append(If(And([literals[i] == 1, literals[j] == 9]), Sum(literals[i+1:j]) == n, True))
    return clauses



clauses = []
lits = [IntVal(i+1) for i in range(9)]
print(lits)
# clauses += exactly_one(lits)
clauses += sum_1_thru_9(lits, 36)

print(*clauses, sep="\n")
s = Solver()

for clause in clauses:
    s.add(clause)

print(s.check())
# print(s)
# print(s.model())
