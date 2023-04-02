
def test_scroll_infinite_page(scraper, base_url):
    """ Checks for scrolling down an infinite page """
    n_scrolls = 5

    scraper.get(base_url + '/infinite_page')
    scraper.scroll_down(n_scrolls, 2)

    paragraphs = scraper.current_page.find_all('div', {'class': 'paragraph'})
    assert len(paragraphs) - 1 == n_scrolls

