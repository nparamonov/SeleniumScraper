from selenium import webdriver

from .base_scraper import BaseScraper


class ChromeScraper(BaseScraper):
    """ Chrome scraper """
    _browser = webdriver.Chrome
    _browser_options = webdriver.ChromeOptions


class FirefoxScraper(BaseScraper):
    """ Chrome scraper """
    _browser = webdriver.Firefox
    _browser_options = webdriver.FirefoxOptions
