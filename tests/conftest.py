import logging
import subprocess
import sys
import time
from collections.abc import Generator
from typing import Any

import pytest

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
def _start_web_app_process() -> Generator[None, Any, None]:
    """Start local web application for tests."""
    process = subprocess.Popen([sys.executable, "tests/web_app/app.py"])  # noqa: S603
    time.sleep(5)

    yield

    process.terminate()
