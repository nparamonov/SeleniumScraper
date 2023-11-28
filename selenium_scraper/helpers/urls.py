from urllib import parse

from selenium_scraper.logger import logger


def update_url_params(url: str, params: dict) -> str:
    """Add or update GET params to provided URL.

    :param url: string of target URL
    :param params: dict containing query params to be added or updated
    :return: string with updated URL

    >>> update_url_params('https://example.com/page?id=1', {'id': '2', 'key': 'val'})
    'https://example.com/page?id=2&key=val'
    """
    url_parts = list(parse.urlparse(url))
    query = dict(parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = parse.urlencode(query)
    return parse.urlunparse(url_parts)


class PageLinks:
    """Internal and external links of the page."""

    default_schemes = ("http", "https")

    def __init__(self, page_url: str, schemes: tuple[str] | None = default_schemes):
        """Initialize PageLinks.

        :param page_url: Full URL of the page where the links are located
        :param schemes: Schemes tuple by which links will be filtered.
            If None, all links will be left. If specified, links with different schemes will be excluded
            (e.g. ('ftp', 'http', 'https', 'ws', 'wss', 'git', 'git+ssh')). Default: ('http', 'https')
        """
        self._page = parse.urlparse(page_url)
        self._schemes = schemes
        self._internal = set()
        self._external = set()

    @property
    def internal(self) -> set:
        """Internal links (other pages on this site)."""
        return self._internal

    @property
    def external(self) -> set:
        """External links (other sites)."""
        return self._external

    def add_link(self, raw_link: str) -> None:
        """Add and process a link.

        :param raw_link: Original link from the page (e.g. '/nparamonov/SeleniumScraper',
            'https://github.com/nparamonov/SeleniumScraper#usage', '//github.com/nparamonov/SeleniumScraper',
            'javascript:void(0)', ...)
        """
        parsed_url = parse.urlparse(raw_link)

        if self._schemes and parsed_url.scheme not in (*self._schemes, ""):
            logger.debug('Link "%s" skipped: wrong scheme', raw_link)
            return

        if parsed_url.netloc and parsed_url.netloc != self._page.netloc:
            if not parsed_url.scheme:
                # https://stackoverflow.com/questions/9646407/two-forward-slashes-in-a-url-src-href-attribute/9646435#9646435
                parsed_url = parsed_url._replace(scheme=self._page.scheme)
            restored_url = parse.urlunparse(parsed_url)
            logger.debug('Link "%s" is external', restored_url)
            self._external.add(restored_url)
            return

        if not parsed_url.netloc and parsed_url.path:
            parsed_url = parsed_url._replace(
                netloc=self._page.netloc,
                scheme=self._page.scheme,
                path=parse.urljoin(self._page.path, parsed_url.path),
            )
            restored_url = parse.urlunparse(parsed_url)
            logger.debug('Link "%s" is internal', restored_url)
            self._internal.add(restored_url)
