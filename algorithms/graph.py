import time
from collections import deque

def bfs(grid, start, end):
    start_time = time.perf_counter()
    rows, cols = len(grid), len(grid[0])

    queue = deque([start])
    visited = set([start])
    parent = {}

    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    while queue:
        current = queue.popleft()

        if current == end:
            break

        r,c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    path = []
    if end in visited:
        node = end
        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)
        path.reverse()

    runtime = time.perf_counter() - start_time

    return {"path": path, "visited_count": len(visited), "runtime": runtime}