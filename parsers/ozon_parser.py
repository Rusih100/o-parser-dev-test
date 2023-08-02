from time import sleep

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from parsers.abstract_parser import AbstractChromeParser
from typing import List, Any, NamedTuple, Optional
from parsers.utils import has_cyrillic


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

    _url = r"https://www.ozon.ru/seller/1/products/"

    def parse_page(self, id_: int) -> None:
        self._driver.close()
        self._driver.start_session({})
        self._driver.get(self._url + f"?miniapp=seller_1&page={id_}")
        sleep(3)

        raw_cards = self._driver.find_elements(
            by=By.XPATH,
            value="//*[@id='paginatorContent']/div/div/div"  # FIX
        )
        print(len(raw_cards))
        for raw_card in raw_cards:
            card = self.parse_card(raw_card)
            if card is not None:
                self._cards.append(card)

        sleep(self._sleep_time * 2)

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
            url=url
        )

    @staticmethod
    def _parse_numbers(string: str) -> int:
        buffer = ""
        for char in string:
            if char.isdigit():
                buffer += char
        return int(buffer)

    def is_last_page(self) -> bool:
        try:
            self._driver.find_element(By.CSS_SELECTOR, '[data-widget="searchResultsError"]')
            return True
        except NoSuchElementException:
            return False

