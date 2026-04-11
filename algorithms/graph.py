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

    return {"path": path, "visited_count": len(visited), "runtime": time.perf_counter() - start_time}

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

    return {"path": path, "visited_count": len(visited), "runtime": time.perf_counter() - start_time}

def bidirectional_bfs(grid, start, end):
    start_time = time.perf_counter()
 
    if not grid or not grid[0]:
        return {"path": [], "visited_count": 0, "runtime": 0.0}
 
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
 
    if start == end:
        return {"path": [start], 
                "visited_count": 1, 
                "runtime": time.perf_counter() - start_time
        }
 
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
 
    start_queue = deque([start])
    end_queue = deque([end])

    start_visited = {start}
    end_visited = {end}

    start_parent = {}
    end_parent = {}

    meeting_node = None

    def expand_frontier(queue, visited, other_visited, parent):
        nonlocal meeting_node

        if not queue:
            return False

        current = queue.popleft()

        if current in other_visited:
            meeting_node = current
            return True
    
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current

                if neighbor in other_visited:
                    meeting_node = neighbor
                    return True

                queue.append(neighbor)

        return False

    while start_queue and end_queue:
        if expand_frontier(start_queue, start_visited, end_visited, start_parent):
            break
        if expand_frontier(end_queue, end_visited, start_visited, end_parent):
            break

    path = []

    if meeting_node is not None:
        # build start -> meeting_node
        left_path = []
        node = meeting_node
        while node != start:
            left_path.append(node)
            node = start_parent[node]
        left_path.append(start)
        left_path.reverse()

        # build meeting_node -> end
        right_path = []
        node = meeting_node
        while node != end:
            if node not in end_parent:
                break
            node = end_parent[node]
            right_path.append(node)

        path = left_path + right_path
 
    return {
        "path": path,
        "visited_count": len(start_visited | end_visited),
        "runtime": time.perf_counter() - start_time,
    }