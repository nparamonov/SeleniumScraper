from abc import ABC, abstractmethod

import psutil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.options import ArgOptions as Options
from selenium.webdriver.common.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from .helpers.urls import PageLinks, update_url_params
from .logger import logger
from .mapping import ScrollMethods

# Unfortunately, selenium does not have a base class containing .service and .options attributes
SupportedSeleniumWebDriver = type[webdriver.Chrome] | type[webdriver.Firefox] | type[webdriver.Edge] | type[webdriver.Ie] | type[webdriver.Safari]


class BaseScraper(ABC):
    """Abstract scraper."""

    @property
    @abstractmethod
    def _browser(self) -> SupportedSeleniumWebDriver:
        """Selenium webdriver class.

        Example:
            from selenium import webdriver

            class ChromeScraper(BaseScraper):
                _browser = webdriver.Chrome
        """

    def __init__(self,
                 options: Options = None,
                 service: Service = None,
                 keep_alive: bool = True) -> None:
        """Initialize driver for scraper.

        :param options: instance of ChromeOptions or FirefoxOptions
        :param service: service object for handling the browser driver if you need to pass extra details
        :param keep_alive: whether to configure RemoteConnection to use HTTP keep-alive
        """
        self._driver = self._browser(options, service, keep_alive)
        logger.info("Start driver. Browser: %s, version: %s",
                    self._driver.capabilities.get("browserName"),
                    self._driver.capabilities.get("browserVersion"))
        self._driver_process = psutil.Process(self._driver.service.process.pid)

    def __del__(self):
        """Close the driver to save the RAM.

        Selenium has some issues with closing the browser. Here's an attempt to kill
        all driver processes, but need more debugging with different browsers
        """
        if not self._driver_process.is_running():
            logger.info("Driver has already been closed")
            return

        logger.info("Trying to quit driver")
        process_children = self._driver_process.children()
        self._driver.quit()

        for process in process_children:
            if process.is_running():
                process.kill()
                logger.warning("Kill process %s", process)

        if not self._driver_process.is_running():
            logger.info("Driver was closed successfully")
            return

        self._driver_process.kill()
        logger.warning("Driver was killed")


class CommonScraper(BaseScraper, ABC):
    """Scraper functionality for all browsers."""
    def get(self, url: str, params: dict | None = None, timeout: float = 5.0):
        """Load a web page in the current browser session.

        :param url: string of target URL
        :param params: dict containing query params for url
        :param timeout: timeout (seconds)
        """
        url = update_url_params(url, params or {})
        self._driver.set_page_load_timeout(timeout)
        self._driver.get(url)
        logger.info("Load %s", url)

    @property
    def driver(self):
        """Access selenium web driver directly."""
        return self._driver

    @property
    def current_page(self) -> BeautifulSoup:
        """Get the source of the current page.

        :return: BeautifulSoup object representing a parsed HTML
        """
        return BeautifulSoup(self._driver.page_source, "lxml")

    def scroll_down(self, method: str = ScrollMethods.end_key) -> None:
        """Scroll current page down once. This is suitable for static pages.

        :param method: way to scroll the page

        There are 3 ways to scroll the page down (`method`):

        - ScrollMethods.js_instant: using javascript window.scrollTo with 'behavior: "instant"'.
            This method scrolls the page immediately (as if teleporting us to the bottom of the page).
            Pros: Highest speed.
            Cons: Triggers for loading new content may not work on some pages.

        - ScrollMethods.js_smooth: using javascript window.scrollTo with 'behavior: "smooth"'.
            The problem of teleportation of the previous method is solved. Slower movement

        - ScrollMethods.end_key: holding down the End key.
            As in the previous method, the movement is smooth.
            Most often 'js_smooth' and 'end_key' should be the same, but in case of some inaccuracies on some pages,
            you can try to replace them.
        """
        if method == ScrollMethods.js_instant:
            self._driver.execute_script(
                'window.scrollTo({left: 0, top: document.body.scrollHeight, behavior: "instant"});',
            )
        elif method == ScrollMethods.js_smooth:
            self._driver.execute_script(
                'window.scrollTo({left: 0, top: document.body.scrollHeight, behavior: "smooth"});',
            )
        elif method == ScrollMethods.end_key:
            self._driver.find_element(By.TAG_NAME, "html").send_keys(Keys.END)
        else:
            msg = "Invalid page scroll method"
            raise ValueError(msg)
        logger.info("Page has been scrolled down")

    def scroll_infinite_page(self, limit: int = 3, timeout: float = 5, method: str = ScrollMethods.end_key) -> None:
        """Scroll current page down for `limit` times (for infinite pages).

        :param limit: number of scrolls
        :param timeout: max waiting time (s)
        :param method: way to scroll the page

        You can specify `limit` > 1 - the number of times the page will be scrolled down.
        If no new content is loaded for more than `timeout` seconds, the loop will end.
        Available scrolling methods can be found in the `BaseScraper.scroll_down` method.
        """
        while limit:
            last_height = self._driver.execute_script("return document.body.scrollHeight")
            self.scroll_down(method)
            limit -= 1
            try:
                wait = WebDriverWait(self._driver, timeout)
                wait.until(
                    lambda driver: driver.execute_script(
                        f"return document.body.scrollHeight > {last_height}",
                    ),
                )
            except TimeoutException:
                logger.warning("New content has not been loaded in %f seconds", timeout)
                break

    def get_all_links(self, schemes: tuple[str] | None = PageLinks.default_schemes) -> PageLinks:
        """Get a helpers.urls.PageLinks object with all links on the current page.

        :param schemes: Schemes tuple by which links will be filtered.
            If None, all links will be left. If specified, links with different schemes will be excluded
            (e.g. ('ftp', 'http', 'https', 'ws', 'wss', 'git', 'git+ssh')). Default: ('http', 'https')
        """
        current_page_links = PageLinks(self._driver.current_url, schemes)

        for link in self.current_page.find_all("a"):
            raw_link = link.get("href")
            current_page_links.add_link(raw_link)

        return current_page_links
