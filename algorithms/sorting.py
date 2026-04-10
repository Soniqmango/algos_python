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
        if low < high:
            pi = partition(a, low, high)
            sort(a, low, pi - 1)
            sort(a, pi + 1, high)

    result = arr.copy()
    sort(result, 0, len(result) - 1)
    metrics.runtime = time.perf_counter() - start

    return result, metrics
