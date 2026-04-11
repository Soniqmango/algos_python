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

# def generate_maze_path_grid(rows, cols, start = (0, 0), end = None, bias = 70):
#     if end == None:
#         end = (rows - 1, cols - 1)

#     grid = [[1 for _ in range(cols)] for _ in range(rows)]

#     r, c = start
#     while (r, c) != (end):
#         grid[r][c] = 0 # clear the obstacle on the path
#         moves = []
#         if r > 0: 
#             for _ in range(100 - bias):
#                 moves.append((r - 1, c)) # up
#         if r < rows - 1: 
#             for _ in range(bias):
#                 moves.append((r + 1, c)) # down
#         if c > 0: 
#             for _ in range(100 - bias):
#                 moves.append((r, c - 1)) # left
#         if c < cols - 1: 
#             for _ in range(bias):
#                 moves.append((r, c + 1))  # right
#         r, c = random.choice(moves) 
#     grid[end[0]][end[1]] = 0  # clear the end cell

#     return grid