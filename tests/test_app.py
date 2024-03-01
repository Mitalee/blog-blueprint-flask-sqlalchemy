import pytest 
from blogexample.app import create_app

@pytest.fixture
def client():
    with create_app().test_client() as client:
        yield client

def test_share_and_track(client):
    # Assuming you have a post with id "test-title"
    post_id = "test-title"
    share_response = client.get(f'/share/{post_id}')
    # Asserting share url generation
    assert share_response.status_code == 200
    share_data = share_response.json
    assert "share_url" in share_data
    share_url = share_data["share_url"]
    share_id = share_url.split("share_id=")[-1]

    # Now, simulating access to shared URL, which should track the share_id
    track_response = client.get(f'/detail/{post_id}?share_id={share_id}')
    assert track_response.status_code == 200

    # Simulating failed wrong share code
    track_response_fail = client.get(f'/detail/{post_id}?share_id=share123')
    assert track_response_fail.status_code == 500