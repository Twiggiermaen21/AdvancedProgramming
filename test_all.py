import unittest

from test_zad_1 import TestIsPalindrome
from test_zad_2 import TestFibonacci
from test_zad_3 import TestCountVowels
from test_zad_4 import TestCalculateDiscount
from test_zad_5 import TestFlattenList
from test_zad_6 import TestWordFrequencies
from test_zad_7 import TestIsPrime


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    test_suite.addTests(loader.loadTestsFromTestCase(TestIsPalindrome))
    test_suite.addTests(loader.loadTestsFromTestCase(TestFibonacci))
    test_suite.addTests(loader.loadTestsFromTestCase(TestCountVowels))
    test_suite.addTests(loader.loadTestsFromTestCase(TestCalculateDiscount))
    test_suite.addTests(loader.loadTestsFromTestCase(TestFlattenList))
    test_suite.addTests(loader.loadTestsFromTestCase(TestWordFrequencies))
    test_suite.addTests(loader.loadTestsFromTestCase(TestIsPrime))
    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
