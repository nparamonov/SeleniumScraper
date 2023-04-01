from typing import Type
import logging
import psutil
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

from .functions import update_url_params

logging.basicConfig(level=logging.DEBUG)


class BaseScraper:
    """ Abstract scraper """
    _browser: Type[webdriver.Chrome] | Type[webdriver.Firefox] = None
    _browser_options: Type[webdriver.ChromeOptions] | Type[webdriver.FirefoxOptions] = None

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
        logging.info('Start driver')
        self._driver_process = psutil.Process(self._driver.service.process.pid)

    @property
    def driver(self):
        """ Access selenium web driver directly """
        return self._driver

    def __del__(self):
        """
        Close the driver to save the RAM

        Selenium has some issues with closing the browser. Here's an attempt to kill
        all driver processes, but need more debugging with different browsers
        """

        if not self._driver_process.is_running():
            logging.info('Driver has already been closed')
            return

        logging.info('Trying to quit driver')
        process_children = self._driver_process.children()
        self._driver.quit()

        for process in process_children:
            if process.is_running():
                process.kill()
                logging.warning(f'Kill process {process}')

        if not self._driver_process.is_running():
            logging.info('Driver was closed successfully')
            return

        self._driver_process.kill()
        logging.warning('Driver was killed')

    def get(self, url: str, params: dict | None = None):
        """
        Load a web page in the current browser session

        :param url: string of target URL
        :param params: dict containing query params for url
        """
        url = update_url_params(url, params or {})
        self._driver.get(url)

    @property
    def current_page(self) -> BeautifulSoup:
        """
        Get the source of the current page
        :return: BeautifulSoup object representing a parsed HTML
        """
        return BeautifulSoup(self._driver.page_source, 'lxml')

    def scroll_down(self, limit: int = 1, timeout: float = 5) -> None:
        """
        Scroll current page down

        :param limit: number of scrolls
        :param timeout: max waiting time (s)

        If called without parameters (`limit` = 1), the page will scroll only 1 time. This is suitable for static
        pages. For infinite pages, you can specify `limit` > 1 - the number of times the page will be scrolled down.
        If no new content is loaded for more than `timeout` seconds, the loop will end
        """
        while limit:
            last_height = self._driver.execute_script('return document.body.scrollHeight')
            self._driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            limit -= 1
            try:
                wait = WebDriverWait(self._driver, timeout)
                wait.until(
                    lambda driver: driver.execute_script(
                        f'return document.body.scrollHeight > {last_height}'
                    )
                )
            except TimeoutException:
                logging.warning(f'New content has not been loaded in {timeout} seconds')
                break
        logging.info('Page has been scrolled down')
