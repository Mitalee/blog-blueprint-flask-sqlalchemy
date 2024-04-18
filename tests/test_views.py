import pytest
from your_application import create_app

@pytest.fixture
def app():
    app = create_app()  # Create the Flask app
    app.config['TESTING'] = True  # Set testing mode to True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Blog" in response.data

def test_show_posts_route(client):
    response = client.get('/posts')
    assert response.status_code == 200



   
