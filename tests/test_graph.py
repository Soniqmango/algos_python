from algorithms.graph import bfs

def test_empty():
    grid = [
        []
    ]
    result = bfs(grid, (0, 0), (0, 0))

    assert result["path"] == []

def test_out_of_grid():
    grid = [
        [0, 1],
        [0, 0]
    ]
    result = bfs(grid, (0, 0), (2, 1))

    assert result["path"] == []
    
def test_simple():
    grid = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    result = bfs(grid, (0, 0), (2, 2))

    assert result["path"][0] == (0, 0)
    assert result["path"][-1] == (2, 2)
    assert len(result["path"]) == 5

def test_no_path():
    grid = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]
    result = bfs(grid, (0, 0), (2, 2))

    assert result["path"] == []

def test_blocked_start():
    grid = [
        [1, 0, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    result = bfs(grid, (0, 0), (2, 2))

    assert result["path"] == []

def test_multiple_paths():
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    result = bfs(grid, (0, 0), (2, 2))

    assert result["path"][0] == (0, 0)
    assert result["path"][-1] == (2, 2)
    assert len(result["path"]) == 5  # shortest path length

def test_path_validity():
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    result = bfs(grid, (0, 0), (2, 2))
    path = result["path"]

    for (r1,c1), (r2,c2) in zip(path,path[1:]):
        assert abs(r2-r1) + abs(c2-c1) == 1 # only one step at a time