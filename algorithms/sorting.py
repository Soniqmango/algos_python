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
