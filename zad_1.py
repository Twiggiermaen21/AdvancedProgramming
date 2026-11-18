def is_palindrome(text: str) -> bool:
    """
    Sprawdza, czy podany ciąg znaków jest palindromem.
    Ignoruje wielkość liter oraz znaki niealfanumeryczne (np. spacje).
    """
    cleaned = "".join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]
