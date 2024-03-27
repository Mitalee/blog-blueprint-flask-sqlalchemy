import pytest
from blogexample.app import create_app, db
from config.test_config import TestConfigOverride
from flask import url_for


@pytest.fixture
def app():
    app = create_app(TestConfigOverride)
    with app.app_context():
        # Ensure app context is pushed
        
        assert app.testing  # Verify that app is in testing mode
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///test.db'  # Verify database URI
        assert app.secret_key == 'test-secret'  # Verify secret key
        db.create_all()
        yield app
        db.drop_all()
        

    
def test_index_route(client, app):
    response = client.get(url_for('blog.index'))
    assert response.status_code == 200
