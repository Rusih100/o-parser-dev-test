from typing import List

import requests
from django.conf import settings

from products_api.parsers.ozon_parser import Card

SEND_MESSAGE_URL = (
    f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
)


def send_parsing_status_alert(cards: List[Card]) -> int:
    text = f"Сохранено: {len(cards)} товаров.\n\n"

    for index, card in enumerate(cards, start=1):
        text += f"{index}. {card.name}\n" f"[Ссылка]({card.url})\n\n"

    data = {
        "chat_id": settings.CHAT_ALERT,
        "text": text,
        "parse_mode": "Markdown",
    }

    response = requests.get(url=SEND_MESSAGE_URL, data=data)
    return response.status_code


def send_error_alert(text: str) -> int:
    data = {
        "chat_id": settings.CHAT_ALERT,
        "text": text,
    }
    response = requests.get(url=SEND_MESSAGE_URL, data=data)
    return response.status_code
