from typing import List, NamedTuple

from celery import shared_task
from products_api.parsers.ozon_parser import OzonParser, Card
from django.conf import settings
from products_api.models import Product


@shared_task
def parsing_product_task(product_count: int) -> None:
    try:
        parser = OzonParser(webdriver_path=settings.PARSER_WEB_DRIVER_PATH)
        products: List[NamedTuple] = parser.parse(count=product_count)
    except Exception as e:
        print(f"Произошла ошибка парсинга: {e}",)
        return

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
            url=product.url
        )



