from algorithms.sorting import insertion_sort
from algorithms.sorting import merge_sort

def test_insertion_sort_empty():
    result, metrics = insertion_sort([])
    assert result == []

def test_insertion_sort_single():
    result, metrics = insertion_sort([5])
    assert result == [5]

def test_insertion_sort_sorted():
    result, metrics = insertion_sort([1, 2, 3, 4])
    assert result == [1, 2, 3, 4]

def test_insertion_sort_reverse():
    result, metrics = insertion_sort([4, 3, 2, 1])
    assert result == [1, 2, 3, 4]

def test_insertion_sort_duplicates():
    result, metrics = insertion_sort([3, 1, 2, 1, 3])
    assert result == [1, 1, 2, 3, 3]

def test_merge_sort_empty():
    result, _ = merge_sort([])
    assert result == []

def test_merge_sort_single():
    result, _ = merge_sort([5])
    assert result == [5]

def test_merge_sort_sorted():
    result, _ = merge_sort([1, 2, 3, 4])
    assert result == [1, 2, 3, 4]

def test_merge_sort_reverse():
    result, _ = merge_sort([4, 3, 2, 1])
    assert result == [1, 2, 3, 4]

def test_merge_sort_duplicates():
    result, _ = merge_sort([3, 1, 2, 1, 3])
    assert result == [1, 1, 2, 3, 3]