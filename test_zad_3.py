import unittest
from zad_3 import count_vowels


class TestCountVowels(unittest.TestCase):
    def test_python(self) -> None:
        self.assertEqual(count_vowels("Python"), 2)

    def test_aeiouy(self) -> None:
        self.assertEqual(count_vowels("AEIOUY"), 6)

    def test_bcd(self) -> None:
        self.assertEqual(count_vowels("bcd"), 0)

    def test_empty(self) -> None:
        self.assertEqual(count_vowels(""), 0)

    def test_proba_zolwia(self) -> None:
        self.assertEqual(count_vowels("Próba żółwia"), 4)


if __name__ == "__main__":
    unittest.main()
