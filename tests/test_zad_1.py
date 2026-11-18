import pytest
from zad_1 import is_palindrome


def test_is_palindrome_kajak() -> None:
    assert is_palindrome("kajak") is True


def test_is_palindrome_sentence() -> None:
    assert is_palindrome("Kobyła ma mały bok") is True


def test_is_palindrome_python() -> None:
    assert is_palindrome("python") is False


def test_is_palindrome_empty_string() -> None:
    assert is_palindrome("") is True


def test_is_palindrome_single_char() -> None:
    assert is_palindrome("A") is True
