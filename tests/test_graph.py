import pytest
from algorithms.graph import bfs, dfs

# ---------- BASIC FAILURE CASES ----------

basic_failure_cases = [
    ([[]], (0, 0), (0, 0)), # empty grid

    ([[0, 1], [0, 0]], (0, 0), (2, 1)), # out of bounds

    ([[1, 0, 0], [1, 1, 0], [0, 0, 0]], (0, 0), (2, 2)), # blocked start

    ([[0, 0, 0], [1, 1, 1], [0, 1, 0]], (0, 0), (2, 2)), # no path
]

@pytest.mark.parametrize("grid,start,end", basic_failure_cases)
def test_bfs_failure_cases(grid, start, end):
    result = bfs(grid, start, end)
    assert result["path"] == []


# ---------- VALID PATHS + VALIDITY ----------

valid_cases = [
    ([[0, 0, 0], [1, 1, 0], [0, 0, 0]], (0, 0), (2, 2)), # simple path

    ([[0, 0, 0], [0, 1, 0], [0, 0, 0]], (0, 0), (2, 2)), # multiple paths
]

@pytest.mark.parametrize("grid,start,end", valid_cases)
def test_bfs_valid_cases(grid, start, end):
    result = bfs(grid, start, end)
    assert result["path"][0] == (0, 0)
    assert result["path"][-1] == (2, 2)
    assert len(result["path"]) == 5
    for (r1, c1), (r2, c2) in zip(result["path"], result["path"][1:]):
        assert abs(r2 - r1) + abs(c2 - c1) == 1
        assert grid[r2][c2] == 0