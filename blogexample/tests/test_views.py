import os

import pytest
from flask import url_for

from blogexample.app import create_app, db
from blogexample.blueprints.blog.forms import AddPostForm
from blogexample.blueprints.blog.models import Post


@pytest.fixture(scope="function")
def client():
    os.environ["CONFIG_TYPE"] = "config.settings.TestingConfig"
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():

            db.create_all()
            yield testing_client  # testing phase
            db.drop_all()


def test_index(client):
    response = client.get(url_for("blog.index"))
    assert response.status_code == 200


def test_add_post(client):
    form_data = {
        "title": "Test Title",
        "body": "Test Body",
        "taglist": "two, new",
        "visible": True,
    }

    response = client.post(
        url_for("blog.add_post"), data=form_data, follow_redirects=True
    )
    assert response.status_code == 200

    # test if the post exists in db
    post = Post.query.filter_by(title="Test Title").first()
    assert post is not None
    assert post.body == "Test Body"


def test_show_posts(client):

    test_post_1 = Post(
        title="First Post", body="Body of Post 1", visible=True, url="first-post"
    )
    test_post_2 = Post(
        title="Second Post", body="Body of Post 1", visible=True, url="second-post"
    )

    db.session.add(test_post_1)
    db.session.add(test_post_2)

    db.session.commit()

    response = client.get(url_for("blog.show_posts"))
    assert response.status_code == 200
    assert b'First Post' in response.data


