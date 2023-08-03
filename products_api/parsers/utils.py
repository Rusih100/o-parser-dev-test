import re


def has_cyrillic(text: str) -> bool:
    return bool(re.search("[а-яА-Я]", text))
