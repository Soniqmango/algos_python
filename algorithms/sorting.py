import time
from utils.metrics import SortMetrics

def insertion_sort(arr):
    a = arr.copy()
    metrics = SortMetrics()

    start = time.perf_counter()

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1

        while j >= 0:
            metrics.comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                metrics.swaps += 1
                j -= 1
            else:
                break

        a[j + 1] = key

    metrics.runtime = time.perf_counter() - start
    return a, metrics

def merge_sort(arr):
    metrics = SortMetrics()
    start = time.perf_counter()

    def merge(left, right):
        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            metrics.comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                metrics.swaps += 1  # approximate move

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    def sort(a):
        if len(a) <= 1:
            return a

        mid = len(a) // 2
        left = sort(a[:mid])
        right = sort(a[mid:])
        return merge(left, right)

    result = sort(arr.copy())
    metrics.runtime = time.perf_counter() - start

    return result, metrics

def quick_sort(arr):
    metrics = SortMetrics()
    start = time.perf_counter()

    def partition(a, low, high):
        pivot = a[high]
        i = low - 1

        for j in range(low, high):
            metrics.comparisons += 1
            if a[j] <= pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    metrics.swaps += 1

        if i + 1 != high:
            a[i + 1], a[high] = a[high], a[i + 1]
            metrics.swaps += 1

        return i + 1

    def sort(a, low, high):
        # Iterative quicksort with median-of-three pivot selection
        stack = []
        stack.append((low, high))
        
        while stack:
            low, high = stack.pop()
            if low < high:
                # Median of three pivot selection
                mid = low + (high - low) // 2
                
                # Sort low, mid, high to find median
                if a[low] > a[mid]:
                    a[low], a[mid] = a[mid], a[low]
                    metrics.swaps += 1
                if a[low] > a[high]:
                    a[low], a[high] = a[high], a[low]
                    metrics.swaps += 1
                if a[mid] > a[high]:
                    a[mid], a[high] = a[high], a[mid]
                    metrics.swaps += 1
                
                # Now a[high] is the median (pivot)
                pi = partition(a, low, high)
                
                # Push right partition first (so left is processed first)
                if pi + 1 < high:
                    stack.append((pi + 1, high))
                if low < pi - 1:
                    stack.append((low, pi - 1))

    result = arr.copy()
    sort(result, 0, len(result) - 1)
    metrics.runtime = time.perf_counter() - start

    return result, metrics


def insertion_sort_steps(arr):
    a = arr.copy()
    metrics = SortMetrics()
    n = len(a)

    yield a.copy(), {
        "action": "start",
        "indices": [],
        "pivot": None,
        "low": 0,
        "high": n - 1,
    }

    for i in range(1, n):
        key = a[i]
        j = i - 1
        yield a.copy(), {
            "action": "select",
            "indices": [i],
            "pivot": i,
            "low": 0,
            "high": i,
        }

        while j >= 0:
            metrics.comparisons += 1
            yield a.copy(), {
                "action": "compare",
                "indices": [j, i],
                "pivot": i,
                "low": 0,
                "high": i,
            }

            if a[j] > key:
                a[j + 1] = a[j]
                metrics.swaps += 1
                yield a.copy(), {
                    "action": "shift",
                    "indices": [j, j + 1],
                    "pivot": i,
                    "low": 0,
                    "high": i,
                }
                j -= 1
            else:
                break

        a[j + 1] = key
        yield a.copy(), {
            "action": "insert",
            "indices": [j + 1],
            "pivot": i,
            "low": 0,
            "high": i,
        }


def merge_sort_steps(arr):
    a = arr.copy()
    metrics = SortMetrics()
    n = len(a)

    def merge(left, mid, right):
        merged = []
        i = left
        j = mid + 1

        while i <= mid and j <= right:
            metrics.comparisons += 1
            yield a.copy(), {
                "action": "compare",
                "indices": [i, j],
                "pivot": mid,
                "low": left,
                "high": right,
            }

            if a[i] <= a[j]:
                merged.append(a[i])
                i += 1
            else:
                merged.append(a[j])
                j += 1
                metrics.swaps += 1

        while i <= mid:
            merged.append(a[i])
            i += 1
        while j <= right:
            merged.append(a[j])
            j += 1

        for k, value in enumerate(merged, start=left):
            a[k] = value
            yield a.copy(), {
                "action": "write",
                "indices": [k],
                "pivot": mid,
                "low": left,
                "high": right,
            }

    def sort(left, right):
        if left >= right:
            return

        mid = (left + right) // 2
        yield from sort(left, mid)
        yield from sort(mid + 1, right)
        yield from merge(left, mid, right)

    yield a.copy(), {
        "action": "start",
        "indices": [],
        "pivot": None,
        "low": 0,
        "high": n - 1,
    }
    yield from sort(0, n - 1)


def quick_sort_steps(arr):
    a = arr.copy()
    metrics = SortMetrics()
    n = len(a)

    def partition(low, high):
        pivot = a[high]
        i = low - 1

        yield a.copy(), {
            "action": "pivot",
            "indices": [high],
            "pivot": high,
            "low": low,
            "high": high,
        }

        for j in range(low, high):
            metrics.comparisons += 1
            yield a.copy(), {
                "action": "compare",
                "indices": [j, high],
                "pivot": high,
                "low": low,
                "high": high,
            }

            if a[j] <= pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    metrics.swaps += 1
                    yield a.copy(), {
                        "action": "swap",
                        "indices": [i, j],
                        "pivot": high,
                        "low": low,
                        "high": high,
                    }

        if i + 1 != high:
            a[i + 1], a[high] = a[high], a[i + 1]
            metrics.swaps += 1
            yield a.copy(), {
                "action": "swap",
                "indices": [i + 1, high],
                "pivot": high,
                "low": low,
                "high": high,
            }

        return i + 1

    def sort(low, high):
        stack = [(low, high)]

        while stack:
            low, high = stack.pop()
            if low >= high:
                continue

            mid = low + (high - low) // 2
            if a[low] > a[mid]:
                metrics.comparisons += 1
                a[low], a[mid] = a[mid], a[low]
                metrics.swaps += 1
                yield a.copy(), {
                    "action": "swap",
                    "indices": [low, mid],
                    "pivot": mid,
                    "low": low,
                    "high": high,
                }
            else:
                metrics.comparisons += 1
                yield a.copy(), {
                    "action": "compare",
                    "indices": [low, mid],
                    "pivot": mid,
                    "low": low,
                    "high": high,
                }

            if a[low] > a[high]:
                metrics.comparisons += 1
                a[low], a[high] = a[high], a[low]
                metrics.swaps += 1
                yield a.copy(), {
                    "action": "swap",
                    "indices": [low, high],
                    "pivot": high,
                    "low": low,
                    "high": high,
                }
            else:
                metrics.comparisons += 1
                yield a.copy(), {
                    "action": "compare",
                    "indices": [low, high],
                    "pivot": high,
                    "low": low,
                    "high": high,
                }

            if a[mid] > a[high]:
                metrics.comparisons += 1
                a[mid], a[high] = a[high], a[mid]
                metrics.swaps += 1
                yield a.copy(), {
                    "action": "swap",
                    "indices": [mid, high],
                    "pivot": high,
                    "low": low,
                    "high": high,
                }
            else:
                metrics.comparisons += 1
                yield a.copy(), {
                    "action": "compare",
                    "indices": [mid, high],
                    "pivot": high,
                    "low": low,
                    "high": high,
                }

            pi = yield from partition(low, high)
            if pi + 1 < high:
                stack.append((pi + 1, high))
            if low < pi - 1:
                stack.append((low, pi - 1))

    yield a.copy(), {
        "action": "start",
        "indices": [],
        "pivot": None,
        "low": 0,
        "high": n - 1,
    }
    yield from sort(0, n - 1)
