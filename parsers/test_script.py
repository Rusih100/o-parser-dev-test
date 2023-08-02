from pathlib import Path

from parsers.ozon_parser import OzonParser

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SELENIUM
SELENIUM_DRIVER_PATH = BASE_DIR / "drivers" / "chromedriver.exe"


if __name__ == "__main__":
    parsers = OzonParser(SELENIUM_DRIVER_PATH)
    data = parsers.parse(10)
    for d in data:
        print(d)
