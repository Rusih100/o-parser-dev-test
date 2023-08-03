from pathlib import Path

from products_api.parsers.ozon_parser import OzonParser

parser = OzonParser(
    Path(r"D:\Pycharm-project\django_ozon_parser\drivers\chromedriver.exe").resolve()
)
products = parser.parse(10)
print(products)
