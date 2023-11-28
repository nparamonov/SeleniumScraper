from selenium_scraper.helpers.urls import update_url_params


def test_add_params():
    """Check adding parameters to the url."""
    res = update_url_params("https://example.com/page", {"id": "2", "key": "val"})
    assert res == "https://example.com/page?id=2&key=val"


def test_change_and_add_params():
    """Check adding and updating existing parameters."""
    res = update_url_params("https://example.com/page?id=1", {"id": "2", "key": "val"})
    assert res == "https://example.com/page?id=2&key=val"


def test_relative_link_params():
    """Check if parameters in relative links are updated correctly."""
    assert update_url_params("/page?id=1", {"id": "2", "key": "val"}) == "/page?id=2&key=val"
    assert update_url_params("page?id=1", {"id": "2", "key": "val"}) == "page?id=2&key=val"
