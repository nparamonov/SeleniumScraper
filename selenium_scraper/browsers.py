from selenium import webdriver

from .scraper import CommonScraper


class ChromeScraper(CommonScraper):
    """ Chrome scraper """
    _browser = webdriver.Chrome
    _browser_options = webdriver.ChromeOptions


class FirefoxScraper(CommonScraper):
    """ Firefox scraper """
    _browser = webdriver.Firefox
    _browser_options = webdriver.FirefoxOptions


class Scraper:
    """ Scraper """
    chrome = ChromeScraper
    firefox = FirefoxScraper
