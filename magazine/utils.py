"""
Moduł narzędziowy utils dla pakietu magazine.
"""


def formatuj_cene(cena: float) -> str:
    """
    Formatuje cenę do czytelnej postaci z walutą PLN.
    """
    return f"{cena:.2f} PLN"


def wypisz_informacje(komunikat: str) -> None:
    """
    Wyświetla komunikat informacyjny.
    """
    print(f"[INFO]: {komunikat}")
