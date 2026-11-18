def polacz_unikalne_do_szescianu(lista1: list[int], lista2: list[int]) -> list[int]:
    """
    Łączy dwie listy w jedną, usuwa duplikaty,
    podnosi każdy element do 3. potęgi i zwraca wynikową listę.
    """
    polaczona = lista1 + lista2
    unikalne = set(polaczona)
    return [element ** 3 for element in unikalne]


if __name__ == "__main__":
    l1: list[int] = [1, 2, 3, 4]
    l2: list[int] = [3, 4, 5, 6]

    wynik: list[int] = polacz_unikalne_do_szescianu(l1, l2)
    print("Lista 1:", l1)
    print("Lista 2:", l2)
    print("Wynik (unikalne elementy podniesione do potęgi 3):", wynik)
