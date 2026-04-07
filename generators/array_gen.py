import random

def generate_random_array(n, low=0, high=1000):
    return [random.randint(low, high) for _ in range(n)]

def generate_sorted_array(n):
    return list(range(n))

def generate_reverse_sorted_array(n):
    return list(range(n, 0, -1))

def generate_nearly_sorted_array(n, swaps=10):
    arr = list(range(n))
    for _ in range(min(swaps, n)):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def generate_duplicate_heavy_array(n, unique_values=5):
    return [random.randint(0, unique_values - 1) for _ in range(n)]