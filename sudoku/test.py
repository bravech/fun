# Testing my logic in z3
from z3 import *
from itertools import combinations


def less_than(literals, n):
    clauses = []
    for comb in combinations(literals, n):
        clauses.append(Or(list(map(Not, [*comb]))))
    return clauses

def greater_than_or_eq(literals, n):
    clauses = []
    for comb in combinations(literals, n):
        clauses.append(And(*comb))
    clauses = [Or(clauses)]
    return clauses

def exactly(literals, n):
    return [
        less_than(literals, n+1),
        greater_than_or_eq(literals, n)
    ]

def not_exactly(literals, n):
    return [Xor(
        And(less_than(literals, n+1)),
        And(greater_than_or_eq(literals, n))
    )]


clauses = []
a = BoolVal(True)
b = BoolVal(True)
c = BoolVal(True)
lits = [a, b, c]
clauses += not_exactly_two(lits)

print(*clauses, sep="\n")
s = Solver()

for clause in clauses:
    s.add(clause)

print(s.check())
# print(s)
# print(s.model())
