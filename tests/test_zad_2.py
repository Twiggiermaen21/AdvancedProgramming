import pytest
from zad_2 import fibonacci


def test_fibonacci_zero() -> None:
    assert fibonacci(0) == 0


def test_fibonacci_one() -> None:
    assert fibonacci(1) == 1


def test_fibonacci_five() -> None:
    assert fibonacci(5) == 5


def test_fibonacci_ten() -> None:
    assert fibonacci(10) == 55


def test_fibonacci_negative() -> None:
    with pytest.raises(ValueError):
        fibonacci(-1)
