Contributing
============

Installing
~~~~~~~~~~

Clone the repository and navigate to the project directory

.. code:: shell

   git clone https://github.com/nparamonov/SeleniumScraper.git
   cd SeleniumScraper

Create a virtual environment:

.. code:: shell

   python -m venv venv

Activate the virtual environment:

.. code:: shell

   # For Linux or macOS:
   source venv/bin/activate
   # For Windows:
   venv\Scripts\activate

Install the dependencies using ``requirements.txt`` file:

.. code:: shell

   pip install -r requirements.txt

Testing
~~~~~~~

Before PR, you should check the tests and add/edit them if necessary.

To test browser behavior, you need to run the local web application at
``tests/web_app/app.py``. This allows you to write tests that do not
depend on any resources, and at the same time customize them as needed.

.. code:: shell

   python tests/web_app/app.py

SeleniumScraper uses Pytest package.

.. code:: shell

   pytest -v tests

You can also check pytest pipeline on GitHub Actions:
`pytest.yml <https://github.com/nparamonov/SeleniumScraper/blob/main/.github/workflows/pytest.yml>`__,
`pytest
workflow <https://github.com/nparamonov/SeleniumScraper/actions/workflows/pytest.yml>`__.

Coverage
^^^^^^^^

Check code coverage

.. code:: shell

   coverage run -m pytest -v tests
   coverage report -m
   coverage html

Linting
~~~~~~~

Also, before each PR it is recommended to analyze your code using
pylint.

.. code:: shell

   pylint selenium_scraper tests

You can also check pylint pipeline on GitHub Actions:
`pylint.yml <https://github.com/nparamonov/SeleniumScraper/blob/main/.github/workflows/pylint.yml>`__,
`pylint
workflow <https://github.com/nparamonov/SeleniumScraper/actions/workflows/pylint.yml>`__.