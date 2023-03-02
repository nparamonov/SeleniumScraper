from typing import Type
from .browsers import ChromeScraper, FirefoxScraper, BaseScraper


class Scraper:
    """ Scraper """
    chrome: Type[BaseScraper] = ChromeScraper
    firefox: Type[BaseScraper] = FirefoxScraper
