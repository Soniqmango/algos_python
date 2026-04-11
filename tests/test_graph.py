import pytest
from algorithms.graph import bfs, dfs, bidirectional_bfs

graph_algorithms = [bfs, dfs, bidirectional_bfs]

# BASIC FAILURE CASES

basic_failure_cases = [
    ([[]], (0, 0), (0, 0)),  # empty grid
    ([[0, 1], [0, 0]], (0, 0), (2, 1)),  # out of bounds
    ([[1, 0, 0], [1, 1, 0], [0, 0, 0]], (0, 0), (2, 2)),  # blocked start
    ([[0, 0, 0], [1, 1, 1], [0, 1, 0]], (0, 0), (2, 2)),  # no path
]

@pytest.mark.parametrize("graph_function", graph_algorithms)
@pytest.mark.parametrize("grid,start,end", basic_failure_cases)
def test_graph_failure_cases(graph_function, grid, start, end):
    result = graph_function(grid, start, end)
    assert result["path"] == []

# VALID PATHS + VALIDITY

valid_cases = [
    ([[0, 0, 0], [1, 1, 0], [0, 0, 0]], (0, 0), (2, 2)),  # simple path
    ([[0, 0, 0], [0, 1, 0], [0, 0, 0]], (0, 0), (2, 2)),  # multiple possible routes
]

@pytest.mark.parametrize("graph_function", graph_algorithms)
@pytest.mark.parametrize("grid,start,end", valid_cases)
def test_graph_valid_cases(graph_function, grid, start, end):
    result = graph_function(grid, start, end)
    path = result["path"]

    assert path[0] == start
    assert path[-1] == end

    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        assert abs(r2 - r1) + abs(c2 - c1) == 1
        assert grid[r2][c2] == 0


# SHORTEST PATH CHECK (specific to some types)

shortest_path_algorithms = [bfs, bidirectional_bfs]

@pytest.mark.parametrize("graph_function", shortest_path_algorithms)
@pytest.mark.parametrize("grid,start,end,expected_length", [
    ([[0, 0, 0], [1, 1, 0], [0, 0, 0]], (0, 0), (2, 2), 5),
    ([[0, 0, 0], [0, 1, 0], [0, 0, 0]], (0, 0), (2, 2), 5),
])
def test_shortest_path_length(graph_function, grid, start, end, expected_length):
    result = graph_function(grid, start, end)
    assert len(result["path"]) == expected_length