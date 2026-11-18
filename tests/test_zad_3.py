import pytest
from zad_3 import count_vowels


def test_count_vowels_python() -> None:
    assert count_vowels("Python") == 2


def test_count_vowels_all_uppercase() -> None:
    assert count_vowels("AEIOUY") == 6


def test_count_vowels_consonants_only() -> None:
    assert count_vowels("bcd") == 0


def test_count_vowels_empty_string() -> None:
    assert count_vowels("") == 0


def test_count_vowels_polish_phrase() -> None:
    assert count_vowels("Próba żółwia") == 4
