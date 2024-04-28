import pytest
from flask import url_for
from ..blogexample import create_app

@pytest.fixture
def client():
  app = create_app(debug=True) #test client for application
  return app.test_client()


def test_index_route(client):

  response = client.get('/') #test the root route
  assert response.status_code == 200
  assert b'Welcome' in response.data 




