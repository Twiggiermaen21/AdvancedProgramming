import sys
import pytest

if __name__ == "__main__":
    print("Uruchamianie testów jednostkowych za pomocą biblioteki pytest...\n")
    exit_code = pytest.main(["-v", "tests"])
    sys.exit(exit_code)
