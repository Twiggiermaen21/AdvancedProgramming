class Property:
    """
    Klasa bazowa opisująca nieruchomość.
    """

    def __init__(
        self, area: float, rooms: int, price: float, address: str
    ) -> None:
        self.area: float = area
        self.rooms: int = rooms
        self.price: float = price
        self.address: str = address

    def __str__(self) -> str:
        return (
            f"Adres: {self.address}, Powierzchnia: {self.area} m², "
            f"Liczba pokoi: {self.rooms}, Cena: {self.price:,.2f} PLN"
        )


class House(Property):
    """
    Klasa opisująca dom (dziedziczy po Property).
    Dodatkowe pole: plot (rozmiar działki, int).
    """

    def __init__(
        self,
        area: float,
        rooms: int,
        price: float,
        address: str,
        plot: int,
    ) -> None:
        super().__init__(area=area, rooms=rooms, price=price, address=address)
        self.plot: int = plot

    def __str__(self) -> str:
        bazowy_opis = super().__str__()
        return (
            f"[Dom]\n"
            f"  {bazowy_opis}\n"
            f"  Powierzchnia działki: {self.plot} m²"
        )


class Flat(Property):
    """
    Klasa opisująca mieszkanie (dziedziczy po Property).
    Dodatkowe pole: floor (piętro, int).
    """

    def __init__(
        self,
        area: float,
        rooms: int,
        price: float,
        address: str,
        floor: int,
    ) -> None:
        super().__init__(area=area, rooms=rooms, price=price, address=address)
        self.floor: int = floor

    def __str__(self) -> str:
        bazowy_opis = super().__str__()
        return (
            f"[Mieszkanie]\n"
            f"  {bazowy_opis}\n"
            f"  Piętro: {self.floor}"
        )


if __name__ == "__main__":
    # Stworzenie obiektu klasy House
    dom = House(
        area=165.5,
        rooms=5,
        price=850000.0,
        address="Katowice, ul. Słoneczna 15",
        plot=800,
    )

    # Stworzenie obiektu klasy Flat
    mieszkanie = Flat(
        area=52.0,
        rooms=2,
        price=430000.0,
        address="Katowice, ul. Francuska 40/12",
        floor=3,
    )

    # Wyświetlenie obiektów
    print("--- Informacje o nieruchomościach ---")
    print(dom)
    print()
    print(mieszkanie)
