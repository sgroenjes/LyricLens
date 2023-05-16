import lyricsgenius
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

GENIUS_CLIENT_ID = os.getenv("GENIUS_CLIENT_ID")
GENIUS_CLIENT_SECRET = os.getenv("GENIUS_CLIENT_SECRET")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

app = FastAPI()

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

@app.get("/lyrics/{artist}/{song_name}")
async def get_lyrics(artist: str, song_name: str):
    song = genius.search_song(song_name, artist)
    if song is not None:
        return {"lyrics": song.lyrics}
    else:
        return {"error": "Song not found"}

