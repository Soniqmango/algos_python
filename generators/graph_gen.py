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

def generate_guaranteed_path_grid(rows, cols, obstacle_prob = 0.5):
    inital_grid = generate_random_obstacle_grid(rows,cols,obstacle_prob=obstacle_prob)
    