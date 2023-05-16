from urllib import parse


def update_url_params(url: str, params: dict) -> str:
    """
    Add or update GET params to provided URL

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
    url = parse.urlunparse(url_parts)
    return url
