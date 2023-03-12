""" Web application for tests """

import uvicorn
from fastapi import FastAPI, responses

app = FastAPI()


@app.get('/ping')
def ping():
    """ Returns 'pong' in body to check if the API is working """
    return responses.PlainTextResponse('pong')


if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', port=8000, reload=True)
