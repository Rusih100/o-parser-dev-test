from abc import ABC, abstractmethod
from time import sleep
from typing import List, NamedTuple, Optional

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class AbstractChromeParser(ABC):
    """
    Абстрактный парсер сайта, для реализации фабричных методов.
    """

    webdriver_url: str = ""
    options: Optional[ChromeOptions] = None
    driver: Optional[Chrome] = None
    sleep_time: int = 3

    user_agent = r"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

    def __init__(self, webdriver_url: str) -> None:
        self.webdriver_url = webdriver_url

    def setup_options(self) -> ChromeOptions:
        options = ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")
        options.add_argument(f"user-agent={self.user_agent}")
        return options

    def _parse_cards_from_page(self, url: str) -> List[NamedTuple]:
        driver = webdriver.Remote(
            command_executor=self.webdriver_url, options=self.setup_options()
        )
        cards: List[NamedTuple] = []

        try:
            driver.get(url)
            sleep(self.sleep_time)

            raw_cards = self.find_cards(driver)
            cards += self._parse_raw_cards(raw_cards)

        except Exception as e:
            ...
        finally:
            driver.close()
            driver.quit()
            sleep(self.sleep_time)

        return cards

    def parse_website(self, objects_count: int) -> List[NamedTuple]:
        return self._parse_all_pages(objects_count=objects_count)

    def _parse_all_pages(self, objects_count: int) -> List[NamedTuple]:
        current_page = 1
        cards: List[NamedTuple] = []

        while len(cards) < objects_count:
            url = self.get_page_url(current_page)

            current_page_cards = self._parse_cards_from_page(url)
            cards += current_page_cards

            current_page += 1
            sleep(self.sleep_time)

            if not current_page_cards:
                break

        return cards[:objects_count]

    def _parse_raw_cards(self, raw_cards: List[WebElement]) -> List[NamedTuple]:
        cards = []

        for raw_card in raw_cards:
            card = self.parse_card(raw_card)
            if card is not None:
                cards.append(card)

        sleep(self.sleep_time)
        return cards

    @property
    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_page_url(self, page: int) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def find_cards(driver: WebDriver) -> List[WebElement]:
        raise NotImplementedError

    @abstractmethod
    def parse_card(self, raw_card: WebElement) -> NamedTuple:
        raise NotImplementedError
