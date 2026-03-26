import pytest

from main import bubble_sort


@pytest.fixture
def sample_numbers() -> list[int]:
    return [5, 1, 4, 2, 8]


def test_bubble_sort_returns_sorted_list(sample_numbers: list[int]) -> None:
    assert bubble_sort(sample_numbers) == [1, 2, 4, 5, 8]


def test_bubble_sort_does_not_modify_original_list(sample_numbers: list[int]) -> None:
    original = sample_numbers.copy()
    bubble_sort(sample_numbers)
    assert sample_numbers == original


def test_bubble_sort_handles_empty_list() -> None:
    assert bubble_sort([]) == []


def test_bubble_sort_keeps_sorted_list_unchanged() -> None:
    already_sorted = [1, 2, 3, 4]
    assert bubble_sort(already_sorted) == [1, 2, 3, 4]


def test_bubble_sort_handles_negative_numbers() -> None:
    values = [0, -10, 5, -3, 2]
    assert bubble_sort(values) == [-10, -3, 0, 2, 5]
