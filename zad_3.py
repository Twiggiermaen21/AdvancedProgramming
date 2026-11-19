def wyswietl_parzyste(liczby):
    """
    Funkcja przyjmuje w parametrze listę liczb
    i wyświetla jedynie elementy parzyste.
    """
    for liczba in liczby:
        if liczba % 2 == 0:
            print(liczba)


if __name__ == "__main__":
    # Utworzenie listy 10 liczb przy użyciu funkcji range (liczby od 1 do 10)
    lista_liczb = list(range(1, 11))
    print(f"Lista wejściowa: {lista_liczb}")
    print("Liczby parzyste:")
    wyswietl_parzyste(lista_liczb)
