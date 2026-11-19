def calculate_discount(price: float | int, discount: float | int) -> float:
    """
    Oblicza cenę po uwzględnieniu rabatu.
    Rabat określany jest jako ułamek dziesiętny z przedziału [0.0, 1.0].
    Dla wartości discount < 0 lub discount > 1 rzuca wyjątek ValueError.
    """
    if discount < 0 or discount > 1:
        raise ValueError(
            "Rabat musi mieścić się w przedziale od 0.0 do 1.0 (od 0% do 100%)"
        )
    if price < 0:
        raise ValueError("Cena nie może być ujemna")

    return float(price * (1 - discount))
