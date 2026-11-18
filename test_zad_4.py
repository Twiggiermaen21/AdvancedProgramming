import unittest
from zad_4 import calculate_discount


class TestCalculateDiscount(unittest.TestCase):
    def test_discount_twenty_percent(self) -> None:
        self.assertEqual(calculate_discount(100, 0.2), 80.0)

    def test_discount_zero_percent(self) -> None:
        self.assertEqual(calculate_discount(50, 0), 50.0)

    def test_discount_hundred_percent(self) -> None:
        self.assertEqual(calculate_discount(200, 1), 0.0)

    def test_discount_negative_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            calculate_discount(100, -0.1)

    def test_discount_greater_than_one_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            calculate_discount(100, 1.5)


if __name__ == "__main__":
    unittest.main()
