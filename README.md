# SeleniumScraper
Tool to speed up writing Selenium parsers

[![license](https://img.shields.io/github/license/nparamonov/SeleniumScraper)](https://github.com/nparamonov/SeleniumScraper/blob/main/LICENSE)
[![pytest](https://img.shields.io/github/actions/workflow/status/nparamonov/SeleniumScraper/pytest.yml?branch=main&label=pytest&logo=pytest)](https://github.com/nparamonov/SeleniumScraper/actions/workflows/pytest.yml)
[![codecov](https://img.shields.io/codecov/c/github/nparamonov/SeleniumScraper/main?label=coverage&logo=codecov&token=YZZ21OI7AG)](https://codecov.io/gh/nparamonov/SeleniumScraper)

## Requirements
- Python 3.10+
- Internet connection
- Chrome or Firefox browser installed on your machine

## Installation
### Installing with PyPI
...

## Usage
### Scraper initialization
You can choose between chrome or firefox browsers
```python
from selenium_scraper import Scraper
scraper = Scraper.chrome()
scraper.get('https://github.com/nparamonov/SeleniumScraper')
```
### Enable logging
SeleniumScraper uses the logging package. You can specify the logging level to see some entries
```python
import logging
logging.basicConfig(level=logging.INFO)
# your code here
```
## Example
...

## Contributing
### Installing
Clone the repository and navigate to the project directory
```shell
git clone https://github.com/nparamonov/SeleniumScraper.git
cd SeleniumScraper
```
Install Poetry (https://python-poetry.org/docs/#installation), e.g.:
```shell
pip install poetry
```
Install the dependencies:
```shell
poetry install
```
Activate the virtual environment:
```shell
poetry shell
```

### Testing
Before PR, you should check the tests and add/edit them if necessary.

SeleniumScraper uses Pytest package.
```shell
pytest -v tests
```

Note that in order to successfully pass the tests, you must have Chrome and Firefox browsers installed on your machine.

You can also check pytest pipeline on GitHub Actions:
[pytest.yml](https://github.com/nparamonov/SeleniumScraper/blob/main/.github/workflows/pytest.yml), 
[pytest workflow](https://github.com/nparamonov/SeleniumScraper/actions/workflows/pytest.yml).

#### Coverage
Check code coverage
```shell
coverage run
coverage report
coverage html
```

## License
This project is licensed under the terms of the Apache License 2.0.