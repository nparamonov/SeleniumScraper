from bs4 import BeautifulSoup

from selenium_scraper import CommonScraper


def test_scraper_get_pong(scraper: CommonScraper, base_url: str) -> None:
    """Check methods `scraper.get` and `scraper.current_page`."""
    scraper.get(base_url + "/ping")
    assert isinstance(scraper.current_page, BeautifulSoup)
    assert scraper.current_page.text == "pong"


def test_driver_get_pong(scraper: CommonScraper, base_url: str) -> None:
    """Check direct access to the selenium web driver."""
    scraper.driver.get(base_url + "/ping")
    assert isinstance(scraper.current_page, BeautifulSoup)
    assert scraper.current_page.text == "pong"
