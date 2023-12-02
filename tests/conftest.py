import logging
import subprocess
import sys
from collections.abc import Generator
from typing import Any

import pytest
import requests

from selenium_scraper import CommonScraper, Scraper

logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="session", params=[Scraper.chrome, Scraper.firefox])
def scraper(request: pytest.FixtureRequest) -> CommonScraper:
    """Scraper init.

    Here you can configure the browser you need.
    Note that the browser must be installed on the device.
    """
    return request.param(headless=True)


@pytest.fixture(scope="session")
def base_url() -> str:
    """Working API for tests from /tests/web_app/app.py."""
    return "http://127.0.0.1:8000"


@pytest.fixture(scope="session", autouse=True)
def _start_web_app_process(base_url: str) -> Generator[None, Any, None]:
    """Start local web application for tests.

    Execute script `tests/web_app/app.py` while the tests are running.
    Poll the API in a loop to run tests only when the application is ready.
    If we were unable to get a response within 10 attempts with a timeout of 0.5 seconds
    (approximately 5 seconds), we terminate the test session with an error.
    """
    process = subprocess.Popen([sys.executable, "tests/web_app/app.py"])  # noqa: S603

    for _ in range(10):
        try:
            response = requests.get(base_url + "/ping", timeout=0.5)
        except requests.exceptions.RequestException:
            continue

        if response.text == "pong":
            break

    else:
        process.terminate()
        pytest.exit("Local web application for tests was not launched", returncode=2)

    yield
    process.terminate()
