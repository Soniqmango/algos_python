# algos-python

Interactive visualizations and benchmarks for classic sorting and pathfinding algorithms, built with Python and Matplotlib.

---

## Algorithms

**Sorting**
- Insertion Sort
- Merge Sort
- Quick Sort (median-of-three, iterative)

**Pathfinding** (grid-based)
- BFS
- DFS
- Bidirectional BFS

---

## Setup

```bash
git clone https://github.com/your-username/algos-python.git
cd algos-python
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

---

## Visualizations

Each algorithm has a step-by-step animation with play/pause, step forward/back, and a speed slider.

---

## Usage

**Run a visualization**
```bash
python3 -m visualizations.sorting_vis   # insertion, merge, quick sort
python3 -m visualizations.graph_vis     # BFS, DFS, bidirectional BFS
```

**Run benchmarks**
```bash
python3 -m benchmarks.bm_sorting        # 5 array types × 3 sizes
python3 -m benchmarks.bm_graph          # 3 grid types × 3 sizes
```

**Run tests**
```bash
pytest tests/
```

---

## Project Structure

```
algorithms/      sorting and graph algorithm implementations
benchmarks/      timing and comparison benchmarks
generators/      array and grid generators (random, sorted, maze, etc.)
tests/           pytest test suite
utils/           SortMetrics and GraphMetrics dataclasses
visualizations/  Matplotlib step-by-step animations
```
