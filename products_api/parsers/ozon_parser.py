from time import sleep
from typing import List, NamedTuple, Optional

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from products_api.parsers.abstract_parser import AbstractChromeParser
from products_api.parsers.utils import has_cyrillic


class Card(NamedTuple):
    name: str
    price: int
    discounted_price: int
    discount: int
    rating: float
    comments_amount: int
    delivery_date: str
    tag: str
    url: str


class OzonParser(AbstractChromeParser):
    @property
    def url(self) -> str:
        return r"https://www.ozon.ru/seller/1/products/"

    def get_page_url(self, page: int) -> str:
        return self.url + f"?miniapp=seller_1&page={page}"

    @staticmethod
    def find_cards(driver: WebDriver) -> List[WebElement]:
        return driver.find_elements(
            by=By.XPATH, value="//*[@id='paginatorContent']/div/div/div"
        )

    def parse_card(self, raw_card: WebElement) -> Optional[Card]:
        # Выдаст все параметры карточки, каждый параметр на своей строке
        body = raw_card.text.split("\n")

        if has_cyrillic(body[0]):  # Проверка на наличие тега
            tag = body.pop(0)
        else:
            tag = ""

        price = self._parse_numbers(body.pop(0))
        discounted_price = self._parse_numbers(body.pop(0))
        discount = self._parse_numbers(body.pop(0))

        delivery_date = body.pop()
        rating, comments_amount = body.pop().split()
        rating = float(rating)
        comments_amount = int(comments_amount)
        name = body.pop()

        url = raw_card.find_element(by=By.TAG_NAME, value="a").get_attribute("href")

        return Card(
            name=name,
            tag=tag,
            price=price,
            discounted_price=discounted_price,
            discount=discount,
            rating=rating,
            comments_amount=comments_amount,
            delivery_date=delivery_date,
            url=url,
        )

    @staticmethod
    def _parse_numbers(string: str) -> int:
        buffer = ""
        for char in string:
            if char.isdigit():
                buffer += char
        return int(buffer)
