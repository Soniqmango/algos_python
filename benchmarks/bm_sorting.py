from algorithms.sorting import insertion_sort, merge_sort, quick_sort
from generators.array_gen import generate_random_array, generate_sorted_array, generate_reverse_sorted_array, generate_nearly_sorted_array, generate_duplicate_heavy_array

def run_benchmarks(function, arr, trials = 5):
    runtimes = []
    comparisons = []
    correct = True

    for _ in range(trials):
        sorted_arr, metrics = function(arr)
        runtimes.append(metrics.runtime)
        comparisons.append(metrics.comparisons)

        if sorted_arr != sorted(arr):
            correct = False
    
    avg_runtime = sum(runtimes) / trials
    avg_comparisons = sum(comparisons) / trials
    return {"avg_runtime": avg_runtime, "avg_comparisons": avg_comparisons, "correct": correct}

def result_to_string(name, size, array_name, result):
    return f"{name}, n={size}, Array Type: {array_name}\nCorrect: {result['correct']}\nAvg Runtime: {result['avg_runtime']:.6f}s\nAvg Comparisons: {result['avg_comparisons']:.1f}\n"

def main():
    sizes = [100, 1000, 5000]

    for size in sizes:
        array_types = [
            ("Random Array", generate_random_array(size)),
            ("Sorted Array", generate_sorted_array(size)),
            ("Reverse Sorted Array", generate_reverse_sorted_array(size)),
            ("Nearly Sorted Array", generate_nearly_sorted_array(size)),
            ("Duplicate Heavy Array", generate_duplicate_heavy_array(size))
        ]

        for array_name, arr in array_types:
            insertion_result = run_benchmarks(insertion_sort, arr)
            merge_result = run_benchmarks(merge_sort, arr)
            quick_result = run_benchmarks(quick_sort, arr)

            print(result_to_string("Insertion Sort", size, array_name, insertion_result))
            print(result_to_string("Merge Sort", size, array_name, merge_result))
            print(result_to_string("Quick Sort", size, array_name, quick_result))
            print("-" * 40 + "\n")

if __name__ == "__main__":
    main()