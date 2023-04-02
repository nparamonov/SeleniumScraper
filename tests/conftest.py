import pytest
from selenium_scraper import Scraper


@pytest.fixture
def scraper():
    """
    Scraper init

    Here you can configure the browser you need.
    Note that the browser must be installed on the device.
    """
    return Scraper.chrome(headless=False)


@pytest.fixture
def base_url():
    """ Working API for tests from /tests/web_app/app.py """
    return 'http://127.0.0.1:8000'
