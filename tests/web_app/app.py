""" Web application for tests """

import uvicorn
from fastapi import FastAPI, responses

app = FastAPI()


@app.get('/ping')
def ping():
    """ Returns 'pong' in body to check if the API is working """
    return responses.PlainTextResponse('pong')


@app.get('/infinite_page')
def infinite_page():
    """ Returns a page that adds content when scrolling down """
    with open('templates/infinite_page.html') as html_file:
        html_source = html_file.read()
    return responses.HTMLResponse(html_source)


if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', port=8000, reload=True)
