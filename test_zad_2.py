import unittest
from zad_2 import fibonacci


class TestFibonacci(unittest.TestCase):
    def test_fibonacci_zero(self) -> None:
        self.assertEqual(fibonacci(0), 0)

    def test_fibonacci_one(self) -> None:
        self.assertEqual(fibonacci(1), 1)

    def test_fibonacci_five(self) -> None:
        self.assertEqual(fibonacci(5), 5)

    def test_fibonacci_ten(self) -> None:
        self.assertEqual(fibonacci(10), 55)

    def test_fibonacci_negative(self) -> None:
        with self.assertRaises(ValueError):
            fibonacci(-1)


if __name__ == "__main__":
    unittest.main()
