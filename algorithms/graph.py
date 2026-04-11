import time
from collections import deque

def bfs(grid, start, end):
    start_time = time.perf_counter()

    # check for empty grid 
    if not grid or not grid[0]:
        return {"path": [], "visited_count": 0, "runtime": 0.0}
    
    # check start/end validity
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    er, ec = end

    if sr not in range(rows) or sc not in range(cols) or er not in range(rows) or ec not in range(cols):
        return {
            "path": [],
            "visited_count": 0,
            "runtime": 0.0,
        }
    
    if grid[sr][sc] == 1 or grid[er][ec] == 1:
        return {
            "path": [],
            "visited_count": 0,
            "runtime": 0.0,
        }
    
    queue = deque([start])
    visited = set([start])
    parent = {}

    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    while queue:
        current = queue.popleft()

        if current == end:
            break

        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if nr in range(rows) and nc in range(cols) and grid[nr][nc] == 0 and neighbor not in visited:
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

def dfs(grid, start, end):
    start_time = time.perf_counter()

    # check for empty grid 
    if not grid or not grid[0]:
        return {"path": [], "visited_count": 0, "runtime": 0.0}
    
    # check start/end validity
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    er, ec = end

    if sr not in range(rows) or sc not in range(cols) or er not in range(rows) or ec not in range(cols):
        return {
            "path": [],
            "visited_count": 0,
            "runtime": 0.0,
        }
    
    if grid[sr][sc] == 1 or grid[er][ec] == 1:
        return {
            "path": [],
            "visited_count": 0,
            "runtime": 0.0,
        }
    
    stack = deque([start])
    visited = set([start])
    parent = {}

    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    while stack:
        current = stack.pop()

        if current == end:
            break

        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if nr in range(rows) and nc in range(cols) and grid[nr][nc] == 0 and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
    
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