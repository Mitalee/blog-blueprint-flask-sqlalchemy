def test_can_get_home_page(client):
    response = client.get("/")
    assert 200 == response.status_code
    assert b"<title>Flask BLOG</title>" in response.data


def test_can_show_posts(client):
    response = client.get("/posts")
    assert 200 == response.status_code
    assert b"<title>Posts</title>" in response.data
