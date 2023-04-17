# SeleniumScraper
Tool to speed up writing Selenium parsers

[![license](https://img.shields.io/github/license/nparamonov/SeleniumScraper)](https://github.com/nparamonov/SeleniumScraper/blob/main/LICENSE)
[![pylint](https://img.shields.io/github/actions/workflow/status/nparamonov/SeleniumScraper/pylint.yml?branch=main&label=pylint&logo=pylint)](https://github.com/nparamonov/SeleniumScraper/actions/workflows/pylint.yml)
[![pytest](https://img.shields.io/github/actions/workflow/status/nparamonov/SeleniumScraper/pytest.yml?branch=main&label=pytest&logo=pytest)](https://github.com/nparamonov/SeleniumScraper/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/gh/nparamonov/SeleniumScraper/branch/main/graph/badge.svg?token=YZZ21OI7AG)](https://codecov.io/gh/nparamonov/SeleniumScraper)

## Requirements
- Python 3.10+
- Internet connection
- Chrome or Firefox browser installed on your machine

## Installation
### Installing with PyPI
...

### Installing from the source
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
Create a virtual environment:
```shell
python -m venv venv
```
Activate the virtual environment:
```shell
# For Linux or macOS:
source venv/bin/activate
# For Windows:
venv\Scripts\activate
```
Install the dependencies using `requirements.txt` file:
```shell
pip install -r requirements.txt
```
### Testing
Before PR, you should check the tests and add/edit them if necessary.

To test browser behavior, you need to run the local web application at `tests/web_app/app.py`.
This allows you to write tests that do not depend on any resources, and at the same time customize them as needed.
```shell
python tests/web_app/app.py
```
SeleniumScraper uses Pytest package.
```shell
pytest -v tests
```
You can also check pytest pipeline on GitHub Actions:
[pytest.yml](https://github.com/nparamonov/SeleniumScraper/blob/main/.github/workflows/pytest.yml), 
[pytest workflow](https://github.com/nparamonov/SeleniumScraper/actions/workflows/pytest.yml).

#### Coverage
Check code coverage
```shell
coverage run -m pytest -v tests
coverage report -m
coverage html
```

### Linting
Also, before each PR it is recommended to analyze your code using pylint.
```shell
pylint selenium_scraper tests
```
You can also check pylint pipeline on GitHub Actions:
[pylint.yml](https://github.com/nparamonov/SeleniumScraper/blob/main/.github/workflows/pylint.yml), 
[pylint workflow](https://github.com/nparamonov/SeleniumScraper/actions/workflows/pylint.yml).

## License
This project is licensed under the terms of the Apache License 2.0.