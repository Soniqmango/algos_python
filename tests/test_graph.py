from algorithms.graph import bfs

def test_bfs_simple():
    grid = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    result = bfs(grid, (0, 0), (2, 2))
    assert result["path"] == [(0, 0), (0, 1)]