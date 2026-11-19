def count_vowels(text: str) -> int:
    """
    Zlicza samogłoski w przekazanym tekście.
    Uwzględnia litery 'y'/'Y' oraz polskie samogłoski.
    W języku polskim litera 'i' przed inną samogłoską
    pełni funkcję zmiękczenia.
    """
    lower = text.lower()
    vowels = "aeiouyąęó"
    count = 0
    i = 0
    while i < len(lower):
        char = lower[i]
        if char in vowels:
            # W polskich słowach 'i' przed samogłoską
            # jest zmiękczeniem (nie osobną samogłoską).
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
