import timeit

import pytest

from selenium_scraper import CommonScraper
from selenium_scraper.mapping import ScrollMethods


@pytest.mark.parametrize("method", [ScrollMethods.end_key, ScrollMethods.js_instant, ScrollMethods.js_smooth])
def test_scroll_infinite_page_methods(scraper: CommonScraper, base_url: str, method: str) -> None:
    """Checks for scrolling down an infinite page with different methods."""
    n_scrolls = 5

    scraper.get(base_url + "/infinite_page")
    scraper.scroll_infinite_page(n_scrolls, 2, method)

    paragraphs = scraper.current_page.find_all("div", {"class": "paragraph"})
    assert len(paragraphs) - 1 >= n_scrolls


def test_scroll_infinite_page_wrong_method(scraper: CommonScraper, base_url: str) -> None:
    """Checks for scrolling down an infinite page with wrong method."""
    n_scrolls = 5

    scraper.get(base_url + "/infinite_page")
    with pytest.raises(ValueError, match="Invalid page scroll method"):
        scraper.scroll_infinite_page(n_scrolls, 2, "my_method")


def test_scroll_infinite_page_timeout_error(scraper: CommonScraper, base_url: str) -> None:
    """Checks for scrolling down an infinite page which causes TimeoutException."""
    n_scrolls = 2
    timeout = 2

    scraper.get(base_url + "/ping")

    s_t = timeit.default_timer()
    scraper.scroll_infinite_page(n_scrolls, timeout)
    e_t = timeit.default_timer()

    duration = int(e_t - s_t)
    assert duration == timeout
