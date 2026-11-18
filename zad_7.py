def is_prime(n: int) -> bool:
    """
    Sprawdza, czy podana liczba całkowita n jest liczbą pierwszą.
    Liczby mniejsze od 2 (w tym 0, 1 oraz liczby ujemne) nie są liczbami pierwszymi.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
