import timeit
import pytest
from selenium_scraper.mapping import ScrollMethods


def test_scroll_infinite_page_end_key(scraper, base_url):
    """ Checks for scrolling down an infinite page with `end_key` method """
    n_scrolls = 5

    scraper.get(base_url + '/infinite_page')
    scraper.scroll_infinite_page(n_scrolls, 2, ScrollMethods.end_key)

    paragraphs = scraper.current_page.find_all('div', {'class': 'paragraph'})
    assert len(paragraphs) - 1 >= n_scrolls


def test_scroll_infinite_page_js_instant(scraper, base_url):
    """ Checks for scrolling down an infinite page with `js_instant` method """
    n_scrolls = 5

    scraper.get(base_url + '/infinite_page')
    scraper.scroll_infinite_page(n_scrolls, 2, ScrollMethods.js_instant)

    paragraphs = scraper.current_page.find_all('div', {'class': 'paragraph'})
    assert len(paragraphs) - 1 >= n_scrolls


def test_scroll_infinite_page_js_smooth(scraper, base_url):
    """ Checks for scrolling down an infinite page with `js_smooth` method """
    n_scrolls = 5

    scraper.get(base_url + '/infinite_page')
    scraper.scroll_infinite_page(n_scrolls, 2, ScrollMethods.js_smooth)

    paragraphs = scraper.current_page.find_all('div', {'class': 'paragraph'})
    assert len(paragraphs) - 1 >= n_scrolls


def test_scroll_infinite_page_wrong_method(scraper, base_url):
    """ Checks for scrolling down an infinite page with wrong method """
    n_scrolls = 5

    scraper.get(base_url + '/infinite_page')
    with pytest.raises(ValueError):
        scraper.scroll_infinite_page(n_scrolls, 2, 'my_method')


def test_scroll_infinite_page_timeout_error(scraper, base_url):
    """ Checks for scrolling down an infinite page which causes TimeoutException """
    n_scrolls = 2
    timeout = 2

    scraper.get(base_url + '/ping')

    s_t = timeit.default_timer()
    scraper.scroll_infinite_page(n_scrolls, timeout)
    e_t = timeit.default_timer()

    duration = int(e_t - s_t)
    assert duration == timeout
