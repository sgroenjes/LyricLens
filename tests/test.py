import pytest
from ../app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to LyricLens" in response.data

def test_get_lyrics(client):
    response = client.post("/lyrics", data={"artist": "Artist Name", "song_name": "Song Name"})
    assert response.status_code == 200
    assert b"Lyrics:" in response.data

def test_get_sentiment(client):
    response = client.post("/sentiment", data={"artist": "Artist Name", "song_name": "Song Name"})
    assert response.status_code == 200
    assert b"Sentiment Analysis:" in response.data

if __name__ == "__main__":
    pytest.main()
