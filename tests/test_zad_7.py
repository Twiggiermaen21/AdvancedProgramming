import pytest
from zad_7 import is_prime


def test_is_prime_two() -> None:
    assert is_prime(2) is True


def test_is_prime_three() -> None:
    assert is_prime(3) is True


def test_is_prime_four() -> None:
    assert is_prime(4) is False


def test_is_prime_zero() -> None:
    assert is_prime(0) is False


def test_is_prime_one() -> None:
    assert is_prime(1) is False


def test_is_prime_five() -> None:
    assert is_prime(5) is True


def test_is_prime_ninety_seven() -> None:
    assert is_prime(97) is True
