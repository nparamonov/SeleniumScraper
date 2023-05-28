""" Web application for tests """

from pathlib import Path
import uvicorn
from fastapi import FastAPI, responses

app = FastAPI()

CURRENT_PATH = Path(__file__).absolute().parent
TEMPLATES_PATH = Path(CURRENT_PATH, 'templates')


def html_response_from_file(file_name: str):
    """
    Returns HTML content
    :param file_name: File name in folder `TEMPLATES_PATH`
    :return: FastAPIs HTMLResponse
    """
    with open(Path(TEMPLATES_PATH, file_name), encoding='utf-8') as html_file:
        html_source = html_file.read()
    return responses.HTMLResponse(html_source)


@app.get('/ping')
def ping():
    """ Returns 'pong' in body to check if the API is working """
    return responses.PlainTextResponse('pong')


@app.get('/infinite_page')
def infinite_page():
    """ Returns a page that adds content when scrolling down """
    return html_response_from_file('infinite_page.html')


@app.get('/page_with_various_links')
def page_with_various_links():
    """ Returns a page with various links """
    return html_response_from_file('page_with_various_links.html')


if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', port=8000, reload=True)
