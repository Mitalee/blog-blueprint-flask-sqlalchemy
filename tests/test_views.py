import pytest
import sys
import os
from flask import url_for

# Add the Flask app directory to sys.path

sys.path.append(os.getcwd())
# sys.path.append("C://Users//shiva//OneDrive//Desktop//khat//blog-blueprint-flask-sqlalchemy//")



# Import create_app function from app module
from blogexample.app import create_app 
from blogexample.blueprints.blog.models import Post, Tag

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def setup_teardown():
    with create_app().app_context():
        yield
        # Teardown if needed

def test_index(client):
    response = client.get(url_for('blog.index'))
    assert response.status_code == 200

# def test_view_post(client):
#     # Create a test post
#     test_post = Post(title="Test Post", body="This is a test post body")
#     test_post.save()

#     # Get the post by its ID
#     response = client.get(url_for('blog.view_post', post_id=test_post.id))

#     # Check if the response is successful
#     assert response.status_code == 200

#     # Check if the post title and body are in the response data
#     assert b"Test Post" in response.data
#     assert b"This is a test post body" in response.data



# if you give me some time i can build test for all routes
