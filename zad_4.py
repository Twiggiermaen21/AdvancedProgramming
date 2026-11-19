def wyswietl_co_drugi(liczby):
    """
    Funkcja przyjmuje w parametrze listę liczb
    i wyświetla co drugi element (indeksy: 0, 2, 4, ...).
    """
    for liczba in liczby[::2]:
        print(liczba)


if __name__ == "__main__":
    # Utworzenie listy 10 liczb przy użyciu funkcji range (liczby od 1 do 10)
    lista_liczb = list(range(1, 11))
    print(f"Lista wejściowa: {lista_liczb}")
    print("Co drugi element:")
    wyswietl_co_drugi(lista_liczb)
