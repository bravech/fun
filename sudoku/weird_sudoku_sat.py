from z3 import *
from itertools import combinations

# SAT solver for the weird sudoku puzzles (see pdfs)

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


graph = open('graph2.txt').read().strip().split('\n')
# graph = open('graph_small.txt').read().strip().split('\n')
graph = list(map(list, graph))

colors = set()

for x in graph:
    for y in x:
        colors.add(y)

regions = {}

for x in colors:
    regions[x] = []


for i in range(len(graph)):
    for j in range(len(graph[0])):
        regions[graph[i][j]].append((i, j))



def solve():
    lits = [[Bool(hex(i)[-1] + hex(j)[-1]) for j in range(len(graph[0]))] for i in range(len(graph))]
    # lits = [
    #     [BoolVal(True), BoolVal(False), BoolVal(False)],
    #     [BoolVal(False), BoolVal(False), BoolVal(True)]
    # ]
    rows, cols = len(lits), len(lits[0])

    clauses = []
    not_clauses = []

    # Not exactly two in each row
    for i in range(rows):
        clauses += exactly([lits[i][j] for j in range(cols)], 2)
    
    # Not exactly two in each column
    for j in range(cols):
        clauses += exactly([lits[i][j] for i in range(rows)], 2)
    
    # Exactly two in each region
    for region in regions:
        clauses += exactly([lits[pos[0]][pos[1]] for pos in regions[region]], 2)

    # # At least 1 star in every row
    # for i in range(rows):
    #     clauses += greater_than_or_eq([lits[i][j] for j in range(cols)], 1)
    
    # # At least 1 star in every column
    # for j in range(cols):
    #     clauses += greater_than_or_eq([lits[i][j] for i in range(rows)], 1)
    
    # Two stars may not be touching
    for i in range(rows):
        for j in range(cols):
            neigh = []
            for a in [-2, 2]:
                for b in range(-2, 3, 1):
                    if i + a >= 0 and i + a < rows and j + b >= 0 and j + b < cols:
                        neigh.append(lits[i+a][j+b])
            for b in [-2, 2]:
                for a in range(-2, 3, 1):
                    if i + a >= 0 and i + a < rows and j + b >= 0 and j + b < cols:
                        neigh.append(lits[i+a][j+b])
            clauses.append(If(lits[i][j], Not(Or(neigh)), True))
    
    s = Solver()
    for clause in clauses:
        s.add(clause)
    
    print(s)
    print(s.check())
    m = s.model()
    words = ['MUMBOJUMBOS', 'UNANIMOUSLY', 'ASNECESSARY', 'COPYRIGHTED', 'ABOLISHMENT', 'WINTERGREEN', 'GREATNEPHEW', 'LIEDETECTOR', 'CYTOPLASMIC', 'DISAPPROVAL', 'SOVIETUNION']
    phrase = ""
    for i in range(len(lits)):
        out = ""
        for j in range(len(lits[0])):
            if is_true(m[lits[i][j]]):
                out += '*'
                phrase += words[i][j]
            else:
                out += '0'
        print(out)
    print(phrase)

solve()




