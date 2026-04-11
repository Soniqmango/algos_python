from algorithms.graph import bfs, dfs, bidirectional_bfs
from generators.graph_gen import generate_empty_graph, generate_random_obstacle_grid, generate_guaranteed_path_grid


def run_benchmarks(function, grid, start, end, trials=5):
    runtimes = []
    visited_counts = []
    path_found = True
    path_lengths = []

    for _ in range(trials):
        result = function(grid, start, end)
        runtimes.append(result["runtime"])
        visited_counts.append(result["visited_count"])

        if result["path"] == []:
            path_found = False
        else:
            path_lengths.append(len(result["path"]))

    avg_runtime = sum(runtimes) / trials
    avg_visited_count = sum(visited_counts) / trials
    avg_path_length = sum(path_lengths) / len(path_lengths) if path_lengths else 0

    return {"avg_runtime": avg_runtime, "avg_visited_count": avg_visited_count, "avg_path_length": avg_path_length, "path found": path_found,}

def result_to_string(name, size, grid_type, result):
    return f"{name}, size={size}, grid={grid_type}\nPath Found: {result['path found']}\nAvg Runtime: {result['avg_runtime']:.6f}s\nAvg Visited Count: {result['avg_visited_count']:.1f}\nAvg Path Length: {result['avg_path_length']:.1f}\n"

def main():
    sizes = [20, 100, 500]

    for size in sizes:
        start = (0, 0)
        end = (size - 1, size - 1)

        empty_grid = generate_empty_graph(size, size)
        random_grid = generate_random_obstacle_grid(size, size)
        guaranteed_grid = generate_guaranteed_path_grid(size, size)

        grid_types = [("Empty Grid", empty_grid),
            ("Random Obstacle Grid", random_grid),
            ("Guaranteed Path Grid", guaranteed_grid),
        ]

        for grid_name, grid in grid_types:
            bfs_result = run_benchmarks(bfs, grid, start, end)
            dfs_result = run_benchmarks(dfs, grid, start, end)
            bidirectional_result = run_benchmarks(bidirectional_bfs, grid, start, end)

            print(result_to_string("BFS", size, grid_name, bfs_result))
            print(result_to_string("DFS", size, grid_name, dfs_result))
            print(result_to_string("Bidirectional BFS", size, grid_name, bidirectional_result))
            print("-" * 40 + "\n")


if __name__ == "__main__":
    main()