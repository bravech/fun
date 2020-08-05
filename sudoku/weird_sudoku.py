
# Inefficient backtracking solver for the weird sudoku puzzles (see pdfs)

graph = open('graph.txt').read().strip().split('\n')
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


grid = [[0] * len(graph[0]) for _ in range(len(graph))]

def possible(i, j, num):
    global grid, graph
    if num == 2:
        for a in range(-1, 2, 1):
            for b in range(-1, 2, 1):
                if i + a >= 0 and i + a < len(grid) and j + b >= 0 and j + b < len(grid[0]):
                    if grid[i+a][j+b] == 2:
                        return False
        count = 0
        for row in range(len(grid)):
            if grid[row][j] == 2:
                count += 1
            if count > 1:
                return False
        count = 0
        for col in range(len(grid[0])):
            if grid[i][col] == 2:
                count += 1
            if count > 1:
                return False
    
        
        count = 0
        for position in regions[graph[i][j]]:
            if grid[position[0]][position[1]] == 2:
                count += 1
            if count > 1:
                return False
    return True

    

def solve():
    global grid, graph
    for row in range(len(graph)):
        for col in range(len(graph[0])):
            if grid[row][col] == 0:
                for digit in [2, 1]:
                    if possible(row, col, digit):
                        grid[row][col] = digit
                        solve()
                        grid[row][col] = 0
                return
            print(grid)


solve()

