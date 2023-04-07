import logging
import pytest
from selenium_scraper import Scraper

logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope='session')
def scraper():
    """
    Scraper init

    Here you can configure the browser you need.
    Note that the browser must be installed on the device.
    """
    return Scraper.chrome(headless=True)


@pytest.fixture(scope='session')
def base_url():
    """ Working API for tests from /tests/web_app/app.py """
    return 'http://127.0.0.1:8000'
