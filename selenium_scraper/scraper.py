from typing import Type
import psutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

from .helpers.urls import update_url_params
from .logger import logger
from .mapping import ScrollMethods


class BaseScraper:
    """ Abstract scraper """
    _browser: Type[webdriver.Chrome] | Type[webdriver.Firefox]
    _browser_options: Type[webdriver.ChromeOptions] | Type[webdriver.FirefoxOptions]

    def __init__(self, *,
                 headless: bool = False,
                 disable_dev_shm_usage: bool = False,
                 no_sandbox: bool = False,
                 args_string: str = ''
                 ) -> None:
        """
        Initialize driver for scraper

        :param headless: ('--headless')
            Do not open the browser so that it runs in the background
        :param disable_dev_shm_usage: ('--disable-dev-shm-usage')
            Write shared memory files into /tmp instead of /dev/shm.
            /dev/shm is an implementation of the traditional shared memory concept.
            The shared memory space is typically too small for Chrome and will cause Chrome to crash
            when rendering large pages. In the past, the size of the shared memory had to be increased.
            Since Chrome Version 65, this is no longer necessary.
            Instead, launch the browser with the --disable-dev-shm-usageflag.
            https://www.cyberciti.biz/tips/what-is-devshm-and-its-practical-usage.html
        :param no_sandbox: ('--no-sandbox')
            Disable sandbox - an additional feature from Chrome:
            https://www.google.com/googlebooks/chrome/med_26.html
        :param args_string:
            A string of additional parameters for arguments not presented above,
            e.g. '--disable-dev-shm-usage --no-sandbox'
        """

        browser_options = self._browser_options()

        arguments = [
            '--headless' * headless,
            '--disable-dev-shm-usage' * disable_dev_shm_usage,
            '--no-sandbox' * no_sandbox,
            args_string
        ]
        arguments_string = ' '.join(filter(None, arguments))

        if arguments_string:
            browser_options.add_argument(arguments_string)

        self._driver = self._browser(options=browser_options)
        logger.info('Start driver. Browser: %s, version: %s',
                    self._driver.capabilities.get("browserName"),
                    self._driver.capabilities.get("browserVersion"))
        self._driver_process = psutil.Process(self._driver.service.process.pid)

    def __del__(self):
        """
        Close the driver to save the RAM

        Selenium has some issues with closing the browser. Here's an attempt to kill
        all driver processes, but need more debugging with different browsers
        """

        if not self._driver_process.is_running():
            logger.info('Driver has already been closed')
            return

        logger.info('Trying to quit driver')
        process_children = self._driver_process.children()
        self._driver.quit()

        for process in process_children:
            if process.is_running():
                process.kill()
                logger.warning('Kill process %s', process)

        if not self._driver_process.is_running():
            logger.info('Driver was closed successfully')
            return

        self._driver_process.kill()
        logger.warning('Driver was killed')


class CommonScraper(BaseScraper):
    """ Scraper functionality for all browsers """
    def get(self, url: str, params: dict | None = None):
        """
        Load a web page in the current browser session

        :param url: string of target URL
        :param params: dict containing query params for url
        """
        url = update_url_params(url, params or {})
        self._driver.get(url)
        logger.info('Load %s', url)

    @property
    def driver(self):
        """ Access selenium web driver directly """
        return self._driver

    @property
    def current_page(self) -> BeautifulSoup:
        """
        Get the source of the current page
        :return: BeautifulSoup object representing a parsed HTML
        """
        return BeautifulSoup(self._driver.page_source, 'lxml')

    def scroll_down(self, method: str = ScrollMethods.end_key) -> None:
        """
        Scroll current page down once. This is suitable for static pages

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
                'window.scrollTo({left: 0, top: document.body.scrollHeight, behavior: "instant"});'
            )
        elif method == ScrollMethods.js_smooth:
            self._driver.execute_script(
                'window.scrollTo({left: 0, top: document.body.scrollHeight, behavior: "smooth"});'
            )
        elif method == ScrollMethods.end_key:
            self._driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
        else:
            raise ValueError('Invalid page scroll method')
        logger.info('Page has been scrolled down')

    def scroll_infinite_page(self, limit: int = 3, timeout: float = 5, method: str = ScrollMethods.end_key) -> None:
        """
            Scroll current page down for `limit` times (for infinite pages)

            :param limit: number of scrolls
            :param timeout: max waiting time (s)
            :param method: way to scroll the page

            You can specify `limit` > 1 - the number of times the page will be scrolled down.
            If no new content is loaded for more than `timeout` seconds, the loop will end.
            Available scrolling methods can be found in the `BaseScraper.scroll_down` method.
        """
        while limit:
            last_height = self._driver.execute_script('return document.body.scrollHeight')
            self.scroll_down(method)
            limit -= 1
            try:
                wait = WebDriverWait(self._driver, timeout)
                wait.until(
                    lambda driver: driver.execute_script(
                        f'return document.body.scrollHeight > {last_height}'
                    )
                )
            except TimeoutException:
                logger.warning('New content has not been loaded in %f seconds', timeout)
                break
