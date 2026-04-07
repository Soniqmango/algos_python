from dataclasses import dataclass

@dataclass
class SortMetrics:
    comparisons: int = 0
    swaps: int = 0
    runtime: float = 0.0