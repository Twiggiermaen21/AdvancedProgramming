import pytest
from zad_6 import word_frequencies


def test_word_frequencies_to_be_or_not_to_be() -> None:
    expected = {"to": 2, "be": 2, "or": 1, "not": 1}
    assert word_frequencies("To be or not to be") == expected


def test_word_frequencies_hello_hello() -> None:
    assert word_frequencies("Hello, hello!") == {"hello": 2}


def test_word_frequencies_empty_string() -> None:
    assert word_frequencies("") == {}


def test_word_frequencies_case_insensitivity() -> None:
    assert word_frequencies("Python Python python") == {"python": 3}


def test_word_frequencies_polish_punctuation() -> None:
    expected = {
        "ala": 1,
        "ma": 2,
        "kota": 1,
        "a": 1,
        "kot": 1,
        "ale": 1,
    }
    assert word_frequencies("Ala ma kota, a kot ma Ale.") == expected
