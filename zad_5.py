from typing import Any


def czy_zawiera(lista_elementow: list[Any], wartosc: int) -> bool:
    """
    Funkcja sprawdza czy przekazana lista zawiera podaną wartość całkowitą.
    """
    return wartosc in lista_elementow


if __name__ == "__main__":
    liczby: list[int] = [10, 20, 30, 40, 50]
    szukana_1: int = 30
    szukana_2: int = 99

    print(
        f"Czy {szukana_1} znajduje się w {liczby}? "
        f"{czy_zawiera(liczby, szukana_1)}"
    )
    print(
        f"Czy {szukana_2} znajduje się w {liczby}? "
        f"{czy_zawiera(liczby, szukana_2)}"
    )
