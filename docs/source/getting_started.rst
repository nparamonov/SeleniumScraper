Getting started
===============

Requirements
------------

- Python ≥ 3.10
- Internet connection
- Chrome or Firefox browser installed on your machine

Installation
------------

Install SeleniumScraper with:

.. code-block:: console

    $ pip install SeleniumScraper

Scraper initialization
----------------------

You can choose between chrome or firefox browsers

.. code-block:: python

    from selenium_scraper import Scraper
    scraper = Scraper.chrome()
    scraper.get('https://github.com/nparamonov/SeleniumScraper')

Enable logging
--------------

SeleniumScraper uses the logging package. You can specify the logging level to see some entries

.. code-block:: python

    import logging
    logging.basicConfig(level=logging.INFO)
    # your code here
