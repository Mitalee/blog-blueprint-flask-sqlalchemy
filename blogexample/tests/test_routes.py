import pytest
# import blogexample
from blogexample.app import create_app,db
from blogexample.blueprints.blog.models import Post

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_index_page(client):
    # Test the index page
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Blog' in response.data

def test_create_post(client):
    # Test creating a new post
    response = client.post('/new', data=dict(
        title='Test Post',
        body='This is a test post.'
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Test Post' in response.data
    assert b'This is a test post.' in response.data

def test_view_post(client):
    # Test viewing a post
    post = Post(title='Another Test Post', body='Another test post body.')
    db.session.add(post)
    db.session.commit()
    
    response = client.get(f'/post/{post.id}')
    assert response.status_code == 200
    assert b'Another Test Post' in response.data
    assert b'Another test post body.' in response.data
