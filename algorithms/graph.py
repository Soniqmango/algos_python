import time
from collections import deque
from utils.metrics import GraphMetrics

def bfs(grid, start, end):
    start_time = time.perf_counter()

    # check for empty grid
    if not grid or not grid[0]:
        return [], GraphMetrics(runtime=time.perf_counter() - start_time)

    # check start/end validity
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    er, ec = end

    if sr not in range(rows) or sc not in range(cols) or er not in range(rows) or ec not in range(cols):
        return [], GraphMetrics(runtime=time.perf_counter() - start_time)

    if grid[sr][sc] == 1 or grid[er][ec] == 1:
        return [], GraphMetrics(runtime=time.perf_counter() - start_time)

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

    metrics = GraphMetrics(
        visited_count=len(visited),
        path_length=len(path),
        runtime=time.perf_counter() - start_time,
    )
    return path, metrics

def dfs(grid, start, end):
    start_time = time.perf_counter()

    # check for empty grid
    if not grid or not grid[0]:
        return [], GraphMetrics(runtime=time.perf_counter() - start_time)

    # check start/end validity
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    er, ec = end

    if sr not in range(rows) or sc not in range(cols) or er not in range(rows) or ec not in range(cols):
        return [], GraphMetrics(runtime=time.perf_counter() - start_time)

    if grid[sr][sc] == 1 or grid[er][ec] == 1:
        return [], GraphMetrics(runtime=time.perf_counter() - start_time)

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

    metrics = GraphMetrics(
        visited_count=len(visited),
        path_length=len(path),
        runtime=time.perf_counter() - start_time,
    )
    return path, metrics

def bidirectional_bfs(grid, start, end):
    start_time = time.perf_counter()

    if not grid or not grid[0]:
        return [], GraphMetrics(runtime=time.perf_counter() - start_time)

    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    er, ec = end

    if sr not in range(rows) or sc not in range(cols) or er not in range(rows) or ec not in range(cols):
        return [], GraphMetrics(runtime=time.perf_counter() - start_time)

    if grid[sr][sc] == 1 or grid[er][ec] == 1:
        return [], GraphMetrics(runtime=time.perf_counter() - start_time)

    if start == end:
        return [start], GraphMetrics(visited_count=1, path_length=1, runtime=time.perf_counter() - start_time)

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

    metrics = GraphMetrics(
        visited_count=len(start_visited | end_visited),
        path_length=len(path),
        runtime=time.perf_counter() - start_time,
    )
    return path, metrics


def bfs_steps(grid, start, end):
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    sr, sc = start
    er, ec = end

    yield {
        "action": "start",
        "current": None,
        "visited": set(),
        "frontier": [],
        "path": [],
        "start": start,
        "end": end,
        "found": False,
    }

    if not grid or not grid[0] or sr not in range(rows) or sc not in range(cols) or er not in range(rows) or ec not in range(cols) or grid[sr][sc] == 1 or grid[er][ec] == 1:
        return

    queue = deque([start])
    visited = {start}
    parent = {}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    yield {
        "action": "enqueue",
        "current": None,
        "visited": visited.copy(),
        "frontier": list(queue),
        "path": [],
        "start": start,
        "end": end,
        "found": False,
    }

    while queue:
        current = queue.popleft()
        yield {
            "action": "visit",
            "current": current,
            "visited": visited.copy(),
            "frontier": list(queue),
            "path": [],
            "start": start,
            "end": end,
            "found": False,
        }

        if current == end:
            break

        r, c = current
        for dr, dc in directions:
            neighbor = (r + dr, c + dc)
            nr, nc = neighbor
            if nr in range(rows) and nc in range(cols) and grid[nr][nc] == 0 and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                yield {
                    "action": "discover",
                    "current": current,
                    "neighbor": neighbor,
                    "visited": visited.copy(),
                    "frontier": list(queue),
                    "path": [],
                    "start": start,
                    "end": end,
                    "found": False,
                }

    path = []
    found = end in visited
    if found:
        node = end
        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)
        path.reverse()

    yield {
        "action": "path",
        "current": end if found else None,
        "visited": visited.copy(),
        "frontier": list(queue),
        "path": path,
        "start": start,
        "end": end,
        "found": found,
    }


def dfs_steps(grid, start, end):
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    sr, sc = start
    er, ec = end

    yield {
        "action": "start",
        "current": None,
        "visited": set(),
        "frontier": [],
        "path": [],
        "start": start,
        "end": end,
        "found": False,
    }

    if not grid or not grid[0] or sr not in range(rows) or sc not in range(cols) or er not in range(rows) or ec not in range(cols) or grid[sr][sc] == 1 or grid[er][ec] == 1:
        return

    stack = deque([start])
    visited = {start}
    parent = {}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    yield {
        "action": "push",
        "current": None,
        "visited": visited.copy(),
        "frontier": list(stack),
        "path": [],
        "start": start,
        "end": end,
        "found": False,
    }

    while stack:
        current = stack.pop()
        yield {
            "action": "visit",
            "current": current,
            "visited": visited.copy(),
            "frontier": list(stack),
            "path": [],
            "start": start,
            "end": end,
            "found": False,
        }

        if current == end:
            break

        r, c = current
        for dr, dc in directions:
            neighbor = (r + dr, c + dc)
            nr, nc = neighbor
            if nr in range(rows) and nc in range(cols) and grid[nr][nc] == 0 and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
                yield {
                    "action": "discover",
                    "current": current,
                    "neighbor": neighbor,
                    "visited": visited.copy(),
                    "frontier": list(stack),
                    "path": [],
                    "start": start,
                    "end": end,
                    "found": False,
                }

    path = []
    found = end in visited
    if found:
        node = end
        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)
        path.reverse()

    yield {
        "action": "path",
        "current": end if found else None,
        "visited": visited.copy(),
        "frontier": list(stack),
        "path": path,
        "start": start,
        "end": end,
        "found": found,
    }


def bidirectional_bfs_steps(grid, start, end):
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    sr, sc = start
    er, ec = end

    yield {
        "action": "start",
        "current": None,
        "start_frontier": [],
        "end_frontier": [],
        "start_visited": set(),
        "end_visited": set(),
        "path": [],
        "start": start,
        "end": end,
        "found": False,
        "meeting_node": None,
    }

    if not grid or not grid[0] or sr not in range(rows) or sc not in range(cols) or er not in range(rows) or ec not in range(cols) or grid[sr][sc] == 1 or grid[er][ec] == 1:
        return

    if start == end:
        yield {
            "action": "path",
            "current": start,
            "start_frontier": [start],
            "end_frontier": [end],
            "start_visited": {start},
            "end_visited": {end},
            "path": [start],
            "start": start,
            "end": end,
            "found": True,
            "meeting_node": start,
        }
        return

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start_queue = deque([start])
    end_queue = deque([end])
    start_visited = {start}
    end_visited = {end}
    start_parent = {}
    end_parent = {}
    meeting_node = None

    def state_frame(action, current=None, discovered=None):
        return {
            "action": action,
            "current": current,
            "neighbor": discovered,
            "start_frontier": list(start_queue),
            "end_frontier": list(end_queue),
            "start_visited": start_visited.copy(),
            "end_visited": end_visited.copy(),
            "path": [],
            "start": start,
            "end": end,
            "found": False,
            "meeting_node": meeting_node,
        }

    yield state_frame("enqueue")

    def expand_frontier(queue, visited, other_visited, parent):
        nonlocal meeting_node
        if not queue:
            return False

        current = queue.popleft()
        yield state_frame("visit", current=current)

        if current in other_visited:
            meeting_node = current
            yield state_frame("meet", current=current)
            return True

        r, c = current
        for dr, dc in directions:
            neighbor = (r + dr, c + dc)
            nr, nc = neighbor
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                yield state_frame("discover", current=current, discovered=neighbor)

                if neighbor in other_visited:
                    meeting_node = neighbor
                    yield state_frame("meet", current=neighbor)
                    return True

        return False

    found = False
    while start_queue and end_queue and meeting_node is None:
        for frame in expand_frontier(start_queue, start_visited, end_visited, start_parent):
            yield frame
            if meeting_node is not None:
                found = True
                break
        if meeting_node is not None:
            break
        for frame in expand_frontier(end_queue, end_visited, start_visited, end_parent):
            yield frame
            if meeting_node is not None:
                found = True
                break

    path = []
    if meeting_node is not None:
        left_path = []
        node = meeting_node
        while node != start:
            left_path.append(node)
            node = start_parent[node]
        left_path.append(start)
        left_path.reverse()

        right_path = []
        node = meeting_node
        while node != end:
            node = end_parent[node]
            right_path.append(node)

        path = left_path + right_path
        found = True

    yield {
        "action": "path",
        "current": meeting_node if found else None,
        "start_frontier": list(start_queue),
        "end_frontier": list(end_queue),
        "start_visited": start_visited.copy(),
        "end_visited": end_visited.copy(),
        "path": path,
        "start": start,
        "end": end,
        "found": found,
        "meeting_node": meeting_node,
    }
