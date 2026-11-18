import unittest
from zad_5 import flatten_list


class TestFlattenList(unittest.TestCase):
    def test_flat_list(self) -> None:
        self.assertEqual(flatten_list([1, 2, 3]), [1, 2, 3])

    def test_nested_list(self) -> None:
        self.assertEqual(flatten_list([1, [2, 3], [4, [5]]]), [1, 2, 3, 4, 5])

    def test_empty_list(self) -> None:
        self.assertEqual(flatten_list([]), [])

    def test_deeply_nested_single_element(self) -> None:
        self.assertEqual(flatten_list([[[1]]]), [1])

    def test_recursive_nested_list(self) -> None:
        self.assertEqual(flatten_list([1, [2, [3, [4]]]]), [1, 2, 3, 4])


if __name__ == "__main__":
    unittest.main()
