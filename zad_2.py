def pomnoz(a: int, b: int) -> int:
    """
    Funkcja przyjmuje 2 liczby całkowite i zwraca wynik ich mnożenia.
    """
    return a * b


if __name__ == "__main__":
    liczba1: int = 6
    liczba2: int = 7
    wynik: int = pomnoz(liczba1, liczba2)
    print(f"Wynik mnożenia {liczba1} * {liczba2} = {wynik}")
