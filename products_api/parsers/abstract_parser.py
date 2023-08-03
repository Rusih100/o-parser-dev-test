from abc import ABC, abstractmethod
from pathlib import Path
from time import sleep
from typing import List, NamedTuple, Optional

from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver.remote.webelement import WebElement


class AbstractChromeParser(ABC):
    _url: str = r""
    _options: Optional[ChromeOptions] = None
    _service: Optional[ChromeService] = None
    _driver: Optional[Chrome] = None
    _sleep_time: int = 5

    _user_agent = r"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

    def __init__(self, webdriver_path: Path) -> None:
        self._options = ChromeOptions()
        self._options.add_argument("--disable-gpu")
        self._options.add_argument("--headless")
        self._options.add_argument(f"user-agent={self._user_agent}")

        self._service = ChromeService(webdriver_path.as_posix())
        self._driver = Chrome(service=self._service, options=self._options)

    def __del__(self):
        self._driver.quit()

    def _open_url(self) -> None:
        self._driver.get(self._url)
        sleep(self._sleep_time)

    def parse(self, count: int) -> List[NamedTuple]:
        self._open_url()

        current_page = 1
        raw_cards = []

        while not self.is_last_page() and len(raw_cards) < count:
            raw_cards += self.parse_page(current_page)
            current_page += 1
            sleep(self._sleep_time)

        raw_cards = raw_cards[:count]
        return self._parse_raw_cards(raw_cards)

    def _parse_raw_cards(self, raw_cards: List[WebElement]) -> List[NamedTuple]:
        cards = []

        for raw_card in raw_cards:
            card = self.parse_card(raw_card)
            if card is not None:
                cards.append(card)

        sleep(self._sleep_time)
        return cards

    @abstractmethod
    def parse_page(self, page_id: int) -> List[WebElement]:
        raise NotImplementedError

    @abstractmethod
    def parse_card(self, raw_card: WebElement) -> NamedTuple:
        raise NotImplementedError

    @abstractmethod
    def is_last_page(self) -> bool:
        raise NotImplementedError
