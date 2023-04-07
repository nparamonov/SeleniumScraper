""" Web application for tests """

from pathlib import Path
import uvicorn
from fastapi import FastAPI, responses

app = FastAPI()

CURRENT_PATH = Path(__file__).absolute().parent
TEMPLATES_PATH = Path(CURRENT_PATH, 'templates')


@app.get('/ping')
def ping():
    """ Returns 'pong' in body to check if the API is working """
    return responses.PlainTextResponse('pong')


@app.get('/infinite_page')
def infinite_page():
    """ Returns a page that adds content when scrolling down """
    with open(Path(TEMPLATES_PATH, 'infinite_page.html'), encoding='utf-8') as html_file:
        html_source = html_file.read()
    return responses.HTMLResponse(html_source)


if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', port=8000, reload=True)
