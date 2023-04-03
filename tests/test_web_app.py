import requests


def test_web_app_ping(base_url: str):
    """ Check if the API is working """
    response = requests.get(base_url + '/ping', timeout=2)

    assert response.status_code == 200
    assert response.text == 'pong'
