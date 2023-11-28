from bs4 import BeautifulSoup


def test_scraper_get_pong(scraper, base_url):
    """Check methods `scraper.get` and `scraper.current_page`."""
    scraper.get(base_url + "/ping")
    assert isinstance(scraper.current_page, BeautifulSoup)
    assert scraper.current_page.text == "pong"


def test_driver_get_pong(scraper, base_url):
    """Check direct access to the selenium web driver."""
    scraper.driver.get(base_url + "/ping")
    assert isinstance(scraper.current_page, BeautifulSoup)
    assert scraper.current_page.text == "pong"
