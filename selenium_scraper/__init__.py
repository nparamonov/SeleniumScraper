from .browsers import ChromeScraper, FirefoxScraper
from .scraper import CommonScraper


class Scraper:
    """Scraper."""
    chrome = ChromeScraper
    firefox = FirefoxScraper
