import argparse
from typing import Any, Optional
import requests


class Brewery:
    """
    Klasa modelu danych reprezentująca browar z Open Brewery DB.
    """

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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Brewery":
        """
        Metoda wytwórcza (fabryczna) tworząca instancję Brewery ze słownika.
        """
        return cls(**data)

    def __str__(self) -> str:
        return (
            f"Browar: {self.name} (ID: {self.id})\n"
            f"  Typ: {self.brewery_type or 'brak'}\n"
            f"  Adres: {self.street or self.address_1 or 'brak'}\n"
            f"  Miasto: {self.city or 'brak'}, "
            f"Kraj: {self.country or 'brak'}\n"
            f"  Telefon: {self.phone or 'brak'}\n"
            f"  Strona WWW: {self.website_url or 'brak'}"
        )


class BreweryApiClient:
    """
    Klasa klienta API odpowiedzialna za komunikację z Open Brewery DB.
    """

    def __init__(
        self, base_url: str = "https://api.openbrewerydb.org/v1/breweries"
    ) -> None:
        self.base_url: str = base_url

    def get_breweries(
        self, city: Optional[str] = None, limit: int = 20
    ) -> list[Brewery]:
        """
        Wysyła żądanie do API i zwraca listę instancji klasy Brewery.
        """
        params: dict[str, Any] = {"per_page": limit}
        if city:
            params["by_city"] = city

        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()

        raw_data: list[dict[str, Any]] = response.json()
        return [Brewery.from_dict(item) for item in raw_data]


class BreweryApp:
    """
    Klasa aplikacji integrująca obsługę wiersza poleceń (CLI),
    klienta API oraz prezentację wyników.
    """

    def __init__(self, api_client: Optional[BreweryApiClient] = None) -> None:
        self.api_client: BreweryApiClient = api_client or BreweryApiClient()

    def parse_arguments(self) -> argparse.Namespace:
        """
        Definiuje i parsuje parametry wiersza poleceń za pomocą argparse.
        """
        parser = argparse.ArgumentParser(
            description="Pobieranie browarów z Open Brewery DB."
        )
        parser.add_argument(
            "--city",
            type=str,
            default=None,
            help="Opcjonalna nazwa miasta do filtrowania (np. --city=Berlin)",
        )
        return parser.parse_args()

    def run(self) -> None:
        """
        Główna metoda uruchamiająca przepływ aplikacji.
        """
        args = self.parse_arguments()
        city_info = f" dla miasta '{args.city}'" if args.city else ""
        print(f"Pobieranie 20 browarów{city_info}...")

        try:
            breweries = self.api_client.get_breweries(city=args.city, limit=20)
        except requests.RequestException as error:
            print(f"Błąd podczas połączenia z API: {error}")
            return

        if not breweries:
            print("Nie znaleziono żadnych browarów.")
            return

        print(f"Pobrano {len(breweries)} obiektów klasy Brewery:\n")
        for index, brewery in enumerate(breweries, start=1):
            print(f"[{index}] {brewery}")
            print("-" * 50)


if __name__ == "__main__":
    app = BreweryApp()
    app.run()
