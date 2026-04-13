from dataclasses import dataclass

@dataclass
class SortMetrics:
    comparisons: int = 0
    swaps: int = 0
    runtime: float = 0.0

@dataclass
class GraphMetrics:
    visited_count: int = 0
    path_length: int = 0
    runtime: float = 0.0