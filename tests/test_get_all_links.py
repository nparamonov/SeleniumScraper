from selenium_scraper import CommonScraper


def test_get_links_from_current_page(scraper: CommonScraper, base_url: str) -> None:
    """Check page with various links."""
    scraper.get(base_url + "/page_with_various_links")
    links = scraper.get_all_links()
    assert links.external == {"http://github.com/nparamonov",
                              "https://github.com/nparamonov/SeleniumScraper"}
    assert links.internal == {base_url + "/page3",
                              base_url + "/about", base_url + "/"}


def test_get_links_from_page_without_links(scraper: CommonScraper, base_url: str) -> None:
    """Check page without links."""
    scraper.get(base_url + "/ping")
    links = scraper.get_all_links()
    assert len(links.internal) == 0
    assert len(links.external) == 0
