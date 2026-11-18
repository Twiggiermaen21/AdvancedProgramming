import argparse
from typing import Any, Optional
import requests


class Brewery:
    id: str
    name: str
    brewery_type: Optional[str]
    address_1: Optional[str]
    address_2: Optional[str]
    address_3: Optional[str]
    city: Optional[str]
    state_province: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    phone: Optional[str]
    website_url: Optional[str]
    state: Optional[str]
    street: Optional[str]

    def __init__(
        self,
        id: str,
        name: str,
        brewery_type: Optional[str] = None,
        address_1: Optional[str] = None,
        address_2: Optional[str] = None,
        address_3: Optional[str] = None,
        city: Optional[str] = None,
        state_province: Optional[str] = None,
        postal_code: Optional[str] = None,
        country: Optional[str] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        phone: Optional[str] = None,
        website_url: Optional[str] = None,
        state: Optional[str] = None,
        street: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.id = id
        self.name = name
        self.brewery_type = brewery_type
        self.address_1 = address_1
        self.address_2 = address_2
        self.address_3 = address_3
        self.city = city
        self.state_province = state_province
        self.postal_code = postal_code
        self.country = country
        self.longitude = float(longitude) if longitude is not None else None
        self.latitude = float(latitude) if latitude is not None else None
        self.phone = phone
        self.website_url = website_url
        self.state = state
        self.street = street

    def __str__(self) -> str:
        return (
            f"Browar: {self.name} (ID: {self.id})\n"
            f"  Typ: {self.brewery_type or 'brak'}\n"
            f"  Adres: {self.street or self.address_1 or 'brak'}\n"
            f"  Miasto: {self.city or 'brak'}, Kraj: {self.country or 'brak'}\n"
            f"  Telefon: {self.phone or 'brak'}\n"
            f"  Strona WWW: {self.website_url or 'brak'}"
        )


def pobierz_browary(city: Optional[str] = None, limit: int = 20) -> list[Brewery]:
    """
    Pobiera listę browarów z API Open Brewery DB z opcjonalnym filtrowaniem po mieście.
    """
    url = "https://api.openbrewerydb.org/v1/breweries"
    params: dict[str, Any] = {"per_page": limit}

    if city:
        params["by_city"] = city

    response = requests.get(url, params=params)
    response.raise_for_status()

    dane = response.json()
    browary: list[Brewery] = [Brewery(**element) for element in dane]
    return browary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pobieranie informacji o browarach z Open Brewery DB"
    )
    parser.add_argument(
        "--city",
        type=str,
        default=None,
        help="Miasto, według którego ograniczone mają zostać pobrane browary",
    )
    args = parser.parse_args()

    miasto_info = f" dla miasta '{args.city}'" if args.city else ""
    print(f"Pobieranie browarów{miasto_info}...")

    lista_browarow: list[Brewery] = pobierz_browary(city=args.city, limit=20)

    if not lista_browarow:
        print("Nie znaleziono żadnych browarów spełniających podane kryteria.")
        return

    print(f"Znaleziono {len(lista_browarow)} browarów:\n")
    for i, browar in enumerate(lista_browarow, start=1):
        print(f"[{i}] {browar}")
        print("-" * 50)


if __name__ == "__main__":
    main()
