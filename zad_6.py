import re


def word_frequencies(text: str) -> dict[str, int]:
    """
    Zlicza wystąpienia poszczególnych słów w podanym tekście.
    Ignoruje wielkość liter oraz znaki interpunkcyjne.
    """
    words = re.findall(r"\w+", text.lower())
    frequencies: dict[str, int] = {}
    for word in words:
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies
