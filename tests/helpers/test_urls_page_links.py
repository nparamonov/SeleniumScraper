from selenium_scraper.helpers.urls import PageLinks

LINKS = ["/", "/", "/about", "page3", "javascript:void(0)", "https://github.com/nparamonov/SeleniumScraper",
         "//github.com/nparamonov"]


def test_links() -> None:
    """Check the processing of various urls."""
    page_links = PageLinks("https://example.com/page1/page2")
    for link in LINKS:
        page_links.add_link(link)

    assert page_links.external == {"https://github.com/nparamonov",
                                   "https://github.com/nparamonov/SeleniumScraper"}
    assert page_links.internal == {"https://example.com/page1/page3",
                                   "https://example.com/about", "https://example.com/"}
