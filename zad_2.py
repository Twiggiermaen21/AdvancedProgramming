def fibonacci(n: int) -> int:
    """
    Zwraca n-ty element ciągu Fibonacciego.
    Dla n < 0 rzuca wyjątek ValueError.
    """
    if n < 0:
        raise ValueError("Liczba n nie może być ujemna")
    if n == 0:
        return 0
    if n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
