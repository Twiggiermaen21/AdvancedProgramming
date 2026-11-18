"""
Główny moduł aplikacji.
Zgodnie z wymaganiem importuje jedynie moduł Product.
"""

from magazine import Product


def main() -> None:
    print("Moduł main uruchomiony pomyślnie.")
    print("Zaimportowano moduł Product:", Product)

    # Utworzenie i wyświetlenie obiektu z modułu Product
    produkt = Product.Product(name="Klawiatura mechaniczna", price=299.99, quantity=10)
    print(produkt)


if __name__ == "__main__":
    main()
