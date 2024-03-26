import requests

ENDPOINT = 'http://localhost:8000/'

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_post():
    payload = {
        "title": "Post 3",
        "body": "Body 3",
        "taglist":"",
        "visible": "y"
    }
    response = requests.post(ENDPOINT + "/add", json=payload)
    assert response.status_code == 200


# def test_can_delete_post():

    