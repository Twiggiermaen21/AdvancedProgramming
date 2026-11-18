import pytest
from zad_4 import calculate_discount


def test_calculate_discount_twenty_percent() -> None:
    assert calculate_discount(100, 0.2) == 80.0


def test_calculate_discount_zero_percent() -> None:
    assert calculate_discount(50, 0) == 50.0


def test_calculate_discount_hundred_percent() -> None:
    assert calculate_discount(200, 1) == 0.0


def test_calculate_discount_negative_raises() -> None:
    with pytest.raises(ValueError):
        calculate_discount(100, -0.1)


def test_calculate_discount_greater_than_one_raises() -> None:
    with pytest.raises(ValueError):
        calculate_discount(100, 1.5)
