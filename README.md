# SeleniumScraper
Tool to speed up writing Selenium parsers

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


## License
This project is licensed under the terms of the Apache License 2.0.