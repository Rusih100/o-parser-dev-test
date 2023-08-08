from typing import List, NamedTuple

from celery import shared_task
from django.conf import settings

from products_api.bot_alerts import send_parsing_status_alert, send_error_alert
from products_api.models import Product
from products_api.parsers.ozon_parser import Card, OzonParser


@shared_task
def parsing_product_task(product_count: int) -> None:
    try:
        parser = OzonParser(webdriver_url=settings.SELENIUM_URL)
        products: List[NamedTuple] = parser.parse(count=product_count)
    except Exception as e:
        send_error_alert(f"Произошла ошибка парсинга: {e}")
        return

    try:
        product: Card
        for product in products:
            Product.objects.create(
                name=product.name,
                price=product.price,
                discounted_price=product.discounted_price,
                rating=product.rating,
                comments_amount=product.comments_amount,
                delivery_date=product.delivery_date,
                tag=product.tag,
                url=product.url,
            )
    except Exception as e:
        send_error_alert(f"Произошла ошибка при добавлении данных в базу данных: {e}")
        return

    products: List[Card]
    send_parsing_status_alert(products)
