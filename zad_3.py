def czy_parzysta(liczba: int) -> bool:
    """
    Funkcja sprawdza czy przekazana liczba jest parzysta.
    Zwraca True jeśli jest parzysta, w przeciwnym razie False.
    """
    return liczba % 2 == 0


if __name__ == "__main__":
    liczba: int = 8
    wynik: bool = czy_parzysta(liczba)

    if wynik:
        print("Liczba parzysta")
    else:
        print("Liczba nieparzysta")

    # Dodatkowy test dla liczby nieparzystej
    liczba_nieparzysta: int = 7
    wynik_nieparzysta: bool = czy_parzysta(liczba_nieparzysta)
    if wynik_nieparzysta:
        print("Liczba parzysta")
    else:
        print("Liczba nieparzysta")
