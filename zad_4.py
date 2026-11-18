def czy_suma_wieksza_lub_rowna(a: int, b: int, c: int) -> bool:
    """
    Funkcja sprawdza czy suma dwóch pierwszych liczb (a + b)
    jest większa lub równa trzeciej liczbie (c).
    """
    return (a + b) >= c


if __name__ == "__main__":
    x: int = 3
    y: int = 5
    z: int = 7
    rezultat: bool = czy_suma_wieksza_lub_rowna(x, y, z)
    print(f"Czy {x} + {y} >= {z}? Odpowiedź: {rezultat}")

    x2, y2, z2 = 2, 3, 10
    rezultat2: bool = czy_suma_wieksza_lub_rowna(x2, y2, z2)
    print(f"Czy {x2} + {y2} >= {z2}? Odpowiedź: {rezultat2}")
