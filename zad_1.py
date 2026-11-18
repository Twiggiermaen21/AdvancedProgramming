def przywitaj(name: str, surname: str) -> str:
    """
    Funkcja przyjmuje imię oraz nazwisko i zwraca sformatowane powitanie.
    """
    return f"Cześć {name} {surname}!"


if __name__ == "__main__":
    powitanie: str = przywitaj("Jan", "Kowalski")
    print(powitanie)
