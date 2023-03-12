import pytest
from selenium_scraper.scraper import Scraper


@pytest.fixture
def scraper():
    """
    Scraper init

    Here you can configure the browser you need.
    Note that the browser must be installed on the device.
    """
    return Scraper.chrome(headless=False)
