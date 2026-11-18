import pytest
from zad_5 import flatten_list


def test_flatten_list_flat() -> None:
    assert flatten_list([1, 2, 3]) == [1, 2, 3]


def test_flatten_list_nested() -> None:
    assert flatten_list([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5]


def test_flatten_list_empty() -> None:
    assert flatten_list([]) == []


def test_flatten_list_deeply_nested_single() -> None:
    assert flatten_list([[[1]]]) == [1]


def test_flatten_list_recursive_nesting() -> None:
    assert flatten_list([1, [2, [3, [4]]]]) == [1, 2, 3, 4]
