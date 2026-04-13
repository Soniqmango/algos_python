import random

def generate_empty_graph(rows, cols):
    if rows <= 0 or cols <= 0:
        return [[]]
    
    return [[0 for _ in range(cols)] for _ in range(rows)]

def generate_random_obstacle_grid(rows, cols, obstacle_prob=0.2):
    if rows <= 0 or cols <= 0:
        return [[]]

    grid = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(1 if random.random() < obstacle_prob else 0)
        grid.append(row)

    return grid

def generate_guaranteed_path_grid(rows, cols, obstacle_prob = 0.4):
    grid = generate_random_obstacle_grid(rows, cols, obstacle_prob=obstacle_prob)

    r, c = 0, 0
    while (r, c) != (rows - 1, cols - 1):
        grid[r][c] = 0 # clear the obstacle on the path
        moves = []
        if r < rows - 1: moves.append((r + 1, c))  # down
        if c < cols - 1: moves.append((r, c + 1))  # right
        r, c = random.choice(moves) 
    grid[rows - 1][cols - 1] = 0  # clear the end cell

    return grid

def generate_maze_grid(rows, cols):
    # Recursive backtracker: carve passages on a grid of cells spaced 2 apart,
    # so walls sit between them. Works best with odd dimensions.
    r = rows if rows % 2 == 1 else rows + 1
    c = cols if cols % 2 == 1 else cols + 1

    grid = [[1] * c for _ in range(r)]

    def carve(row, col):
        grid[row][col] = 0
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < r and 0 <= nc < c and grid[nr][nc] == 1:
                grid[row + dr // 2][col + dc // 2] = 0
                carve(nr, nc)

    import sys
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old_limit, r * c))
    carve(1, 1)
    sys.setrecursionlimit(old_limit)

    # Trim to requested size
    return [grid[row][:cols] for row in range(rows)]