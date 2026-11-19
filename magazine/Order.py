"""
Moduł Order pakietu magazine.
Importuje moduł utils.
"""

try:
    from magazine import utils
except ModuleNotFoundError:
    try:
        from . import utils
    except (ImportError, ValueError):
        import utils


class Order:
    """
    Klasa opisująca zamówienie w magazynie.
    """

    def __init__(self, order_id: int, total_amount: float) -> None:
        self.order_id: int = order_id
        self.total_amount: float = total_amount

    def __str__(self) -> str:
        sformatowana_kwota = utils.formatuj_cene(self.total_amount)
        return (
            f"Zamówienie nr {self.order_id}, "
            f"Łączna kwota: {sformatowana_kwota}"
        )


if __name__ == "__main__":
    o = Order(101, 7200.50)
    print(o)
