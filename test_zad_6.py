import unittest
from zad_6 import word_frequencies


class TestWordFrequencies(unittest.TestCase):
    def test_to_be_or_not_to_be(self) -> None:
        expected = {"to": 2, "be": 2, "or": 1, "not": 1}
        self.assertEqual(word_frequencies("To be or not to be"), expected)

    def test_hello_hello(self) -> None:
        expected = {"hello": 2}
        self.assertEqual(word_frequencies("Hello, hello!"), expected)

    def test_empty_string(self) -> None:
        self.assertEqual(word_frequencies(""), {})

    def test_python_case_sensitivity(self) -> None:
        expected = {"python": 3}
        self.assertEqual(word_frequencies("Python Python python"), expected)

    def test_polish_text_with_punctuation(self) -> None:
        # "Ala ma kota, a kot ma Ale." -> ignorowanie kropek i przecinków, małe litery
        expected = {
            "ala": 1,
            "ma": 2,
            "kota": 1,
            "a": 1,
            "kot": 1,
            "ale": 1,
        }
        self.assertEqual(word_frequencies("Ala ma kota, a kot ma Ale."), expected)


if __name__ == "__main__":
    unittest.main()
