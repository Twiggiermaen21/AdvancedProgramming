# Wersja 1: Wykorzystując pętlę for
def pomnoz_przez_dwa_petla(liczby):
    """
    Funkcja przyjmuje w parametrze listę liczb,
    mnoży każdy element przez 2 za pomocą pętli for i zwraca nową listę.
    """
    wynik = []
    for liczba in liczby:
        wynik.append(liczba * 2)
    return wynik


# Wersja 2: Wykorzystując listę składaną (list comprehension)
def pomnoz_przez_dwa_comprehension(liczby):
    """
    Funkcja przyjmuje w parametrze listę liczb,
    mnoży każdy element przez 2 za pomocą listy składanej i zwraca nową listę.
    """
    return [liczba * 2 for liczba in liczby]


if __name__ == "__main__":
    lista_liczb = [2, 5, 7, 10, 14]

    print("Lista początkowa:", lista_liczb)

    # Test wersji 1
    wynik_petla = pomnoz_przez_dwa_petla(lista_liczb)
    print("Wynik (pętla for):", wynik_petla)

    # Test wersji 2
    wynik_comprehension = pomnoz_przez_dwa_comprehension(lista_liczb)
    print("Wynik (lista składana):", wynik_comprehension)
