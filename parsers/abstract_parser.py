from abc import ABC, abstractmethod
from pathlib import Path

from selenium.webdriver import ChromeOptions, Chrome, ChromeService
from time import sleep

from typing import Optional, List, Any

from selenium.webdriver.remote.webelement import WebElement


class AbstractChromeParser(ABC):

    _url: str = r""
    _options: Optional[ChromeOptions] = None
    _service: Optional[ChromeService] = None
    _driver: Optional[Chrome] = None
    _sleep_time: int = 5

    _start_page: int = 1
    _stop_page: int = -1
    _current_page: int = _start_page
    _cards: List[Any] = []

    _user_agent = r"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

    def __init__(self, webdriver_path: Path) -> None:
        self._options = ChromeOptions()

        self._options.add_argument('--headless=new')
        self._options.add_argument(f"user-agent={self._user_agent}")

        self._service = ChromeService(webdriver_path.as_posix())
        self._driver = Chrome(service=self._service, options=self._options)

    def __del__(self):
        self._driver.quit()
        self._options = None
        self._service = None
        self._driver = None

    @property
    def cards(self):
        return self._cards

    def _open_url(self) -> None:
        self._driver.get(self._url)
        sleep(self._sleep_time)

    def parse(self) -> None:
        self._open_url()

        while not self.is_last_page():
            self.parse_page(self._current_page)
            self._current_page += 1

            sleep(self._sleep_time)

    @abstractmethod
    def parse_page(self, id_: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def parse_card(self, raw_card: WebElement) -> Any:
        raise NotImplementedError

    @abstractmethod
    def is_last_page(self) -> bool:
        raise NotImplementedError
