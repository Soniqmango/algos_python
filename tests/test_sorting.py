import pytest
from algorithms.sorting import insertion_sort, merge_sort, quick_sort

# all sorting types
sorting_types = [insertion_sort, merge_sort, quick_sort]

@pytest.mark.parametrize("sort_function", sorting_types)
def test_sort_empty(sort_function):
    result, _ = sort_function([])
    assert result == []

@pytest.mark.parametrize("sort_function", sorting_types)
def test_sort_single(sort_function):
    result, _ = sort_function([5])
    assert result == [5]

@pytest.mark.parametrize("sort_function", sorting_types)
def test_sort_sorted(sort_function):
    result, _ = sort_function([1, 2, 3, 4])
    assert result == [1, 2, 3, 4]

@pytest.mark.parametrize("sort_function", sorting_types)
def test_sort_reverse(sort_function):
    result, _ = sort_function([4, 3, 2, 1])
    assert result == [1, 2, 3, 4]

@pytest.mark.parametrize("sort_function", sorting_types)
def test_sort_duplicates(sort_function):
    result, _ = sort_function([3, 1, 2, 1, 3])
    assert result == [1, 1, 2, 3, 3]

@pytest.mark.parametrize("sort_function", sorting_types)
def test_sort_all_same(sort_function):
    result, _ = sort_function([2, 2, 2, 2])
    assert result == [2, 2, 2, 2]