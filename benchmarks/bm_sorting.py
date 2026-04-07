from algorithms.sorting import insertion_sort, merge_sort
from generators.array_gen import generate_random_array

def main():
    arr = generate_random_array(1000)

    sorted1, m1 = insertion_sort(arr)
    sorted2, m2 = merge_sort(arr)

    print("Insertion correct:", sorted1 == sorted(arr))
    print("Merge correct:", sorted2 == sorted(arr))

    print("\nInsertion Sort:")
    print("Comparisons:", m1.comparisons)
    print("Runtime:", m1.runtime)

    print("\nMerge Sort:")
    print("Comparisons:", m2.comparisons)
    print("Runtime:", m2.runtime)

if __name__ == "__main__":
    main()