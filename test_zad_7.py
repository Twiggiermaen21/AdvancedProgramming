import unittest
from zad_7 import is_prime


class TestIsPrime(unittest.TestCase):
    def test_two(self) -> None:
        self.assertTrue(is_prime(2))

    def test_three(self) -> None:
        self.assertTrue(is_prime(3))

    def test_four(self) -> None:
        self.assertFalse(is_prime(4))

    def test_zero(self) -> None:
        self.assertFalse(is_prime(0))

    def test_one(self) -> None:
        self.assertFalse(is_prime(1))

    def test_five(self) -> None:
        self.assertTrue(is_prime(5))

    def test_ninety_seven(self) -> None:
        self.assertTrue(is_prime(97))


if __name__ == "__main__":
    unittest.main()
