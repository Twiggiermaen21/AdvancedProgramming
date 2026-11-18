def wyswietl_imiona(imiona):
    """
    Funkcja przyjmuje w parametrze listę 5 imion
    i wyświetla każde z nich w nowej linii.
    """
    for imie in imiona:
        print(imie)


if __name__ == "__main__":
    lista_imion = ["Anna", "Jan", "Katarzyna", "Piotr", "Zofia"]
    wyswietl_imiona(lista_imion)
