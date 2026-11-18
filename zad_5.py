from typing import Any


def flatten_list(nested_list: list[Any]) -> list[Any]:
    """
    Spłaszcza zagnieżdżoną listę do postaci listy jednowymiarowej.
    """
    result: list[Any] = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result
