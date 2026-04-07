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