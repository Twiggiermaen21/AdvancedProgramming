"""
Moduł Product pakietu magazine.
Importuje moduł utils.
"""

try:
    from magazine import utils
except ModuleNotFoundError:
    try:
        from . import utils
    except (ImportError, ValueError):
        import utils


class Product:
    """
    Klasa opisująca produkt w magazynie.
    """

    def __init__(self, name: str, price: float, quantity: int = 0) -> None:
        self.name: str = name
        self.price: float = price
        self.quantity: int = quantity

    def __str__(self) -> str:
        sformatowana_cena = utils.formatuj_cene(self.price)
        return f"Produkt: {self.name}, Cena: {sformatowana_cena}, Ilość: {self.quantity}"


if __name__ == "__main__":
    p = Product("Laptop", 3500.0, 5)
    print(p)
