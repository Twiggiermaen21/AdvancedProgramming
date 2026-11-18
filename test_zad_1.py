import unittest
from zad_1 import is_palindrome


class TestIsPalindrome(unittest.TestCase):
    def test_kajak(self) -> None:
        self.assertTrue(is_palindrome("kajak"))

    def test_kobyla_ma_maly_bok(self) -> None:
        self.assertTrue(is_palindrome("Kobyła ma mały bok"))

    def test_python(self) -> None:
        self.assertFalse(is_palindrome("python"))

    def test_empty_string(self) -> None:
        self.assertTrue(is_palindrome(""))

    def test_single_character(self) -> None:
        self.assertTrue(is_palindrome("A"))


if __name__ == "__main__":
    unittest.main()
