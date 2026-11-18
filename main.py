import unittest
from test_all import suite

if __name__ == "__main__":
    print("Uruchamianie wszystkich testów jednostkowych (Zadania 1-7)...\n")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    if not result.wasSuccessful():
        exit(1)
