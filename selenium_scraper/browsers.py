from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from .scraper import CommonScraper


class ChromeScraper(CommonScraper):
    """Chrome scraper."""
    _browser = webdriver.Chrome
    _browser_options = webdriver.ChromeOptions

    def __init__(self,
                 options: ChromeOptions = None,
                 service: ChromeService = None,
                 keep_alive: bool = True,
                 *,
                 headless: bool = False,
                 disable_dev_shm_usage: bool = False,
                 no_sandbox: bool = True,
                 no_default_browser_check: bool = True,
                 no_first_run: bool = True):
        """Initialize Chrome driver for scraper.

        :param options: instance of ChromeOptions
        :param service: service object for handling the browser driver if you need to pass extra details
        :param keep_alive: whether to configure RemoteConnection to use HTTP keep-alive

        You can configure ChromeOptions however you like with Chrome arguments:
        https://peter.sh/experiments/chromium-command-line-switches/.
        For your convenience, some commonly used useful arguments are moved to the class init:

        :param headless: ('--headless')
            Do not open the browser so that it runs in the background
        :param disable_dev_shm_usage: ('--disable-dev-shm-usage')
            Write shared memory files into /tmp instead of /dev/shm.
            /dev/shm is an implementation of the traditional shared memory concept.
            The shared memory space is typically too small for Chrome and will cause Chrome to crash
            when rendering large pages. In the past, the size of the shared memory had to be increased.
            Since Chrome Version 65, this is no longer necessary.
            https://www.cyberciti.biz/tips/what-is-devshm-and-its-practical-usage.html
        :param no_sandbox: ('--no-sandbox')
            Disable sandbox - an additional feature from Chrome:
            https://www.google.com/googlebooks/chrome/med_26.html
        :param no_default_browser_check: ('--no-default-browser-check')
            Disables the default browser check to avoid having the default browser info-bar displayed
        :param no_first_run: ('--no-first-run')
            Skip First Run tasks, whether or not it`s actually the First Run
        """
        if not options:
            options = self._browser_options()

        arguments = {
            "--headless": headless,
            "--disable-dev-shm-usage": disable_dev_shm_usage,
            "--no-sandbox": no_sandbox,
            "--no-default-browser-check": no_default_browser_check,
            "--no-first-run": no_first_run,
        }
        for argument, enabled in arguments.items():
            if enabled and argument not in options.arguments:
                options.add_argument(argument)

        super().__init__(options, service, keep_alive)


class FirefoxScraper(CommonScraper):
    """Firefox scraper."""
    _browser = webdriver.Firefox
    _browser_options = webdriver.FirefoxOptions

    def __init__(self,
                 options: FirefoxOptions = None,
                 service: FirefoxService = None,
                 keep_alive: bool = True,
                 *,
                 headless: bool = False):
        """Initialize Firefox driver for scraper.

        :param options: instance of FirefoxOptions
        :param service: service object for handling the browser driver if you need to pass extra details
        :param keep_alive: whether to configure RemoteConnection to use HTTP keep-alive

        You can configure FirefoxOptions however you like with Firefox arguments:
        https://developer.mozilla.org/en-US/docs/Web/WebDriver/Capabilities/firefoxOptions.
        For your convenience, some commonly used useful arguments are moved to the class init:

        :param headless: ('-headless')
            Do not open the browser so that it runs in the background
        """
        if not options:
            options = self._browser_options()

        arguments = {
            "-headless": headless,
        }
        for argument, enabled in arguments.items():
            if enabled and argument not in options.arguments:
                options.add_argument(argument)

        super().__init__(options, service, keep_alive)
