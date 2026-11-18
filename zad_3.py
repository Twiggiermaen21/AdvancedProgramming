def count_vowels(text: str) -> int:
    """
    Zlicza samogłoski w przekazanym tekście (uwzględniając litery 'y'/'Y' oraz polskie samogłoski).
    W języku polskim litera 'i' poprzedzająca inną samogłoskę pełni funkcję zmiękczenia
    (np. w słowie 'żółwia' samogłoskami są 'ó' oraz 'a', co łącznie ze słowem 'Próba' daje 4 samogłoski).
    """
    lower = text.lower()
    vowels = "aeiouyąęó"
    count = 0
    i = 0
    while i < len(lower):
        char = lower[i]
        if char in vowels:
            # W polskich słowach 'i' przed samogłoską jest zmiękczeniem (nie osobną samogłoską),
            # o ile słowo zawiera również spółgłoski (wyklucza to ciągi czystych samogłosek jak AEIOUY)
            if (
                char == "i"
                and i + 1 < len(lower)
                and lower[i + 1] in vowels
                and any(c.isalpha() and c not in vowels for c in lower)
            ):
                pass
            else:
                count += 1
        i += 1
    return count
