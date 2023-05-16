import lyricsgenius
from fastapi import FastAPI
import os
from dotenv import load_dotenv
import re
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from flask import Flask, jsonify, request

load_dotenv()  # take environment variables from .env.

GENIUS_CLIENT_ID = os.getenv("GENIUS_CLIENT_ID")
GENIUS_CLIENT_SECRET = os.getenv("GENIUS_CLIENT_SECRET")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

# Download the stopwords from NLTK
nltk.download('stopwords')
# Download the VADER lexicon
nltk.download('vader_lexicon')

stop_words = set(stopwords.words('english'))
sia = SentimentIntensityAnalyzer()

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, timeout=15)

@app.route("/api/lyrics", methods=["POST"])
def get_lyrics():
  data = request.get_json()  # Get data from JSON payload
  artist = data.get("artist")
  song_name = data.get("song_name")
  song = genius.search_song(song_name, artist)
  if song is not None:
    cleaned_lyrics = clean_lyrics(song.lyrics)
    return jsonify({"lyrics": cleaned_lyrics})
  else:
    return jsonify({"error": "Song not found"}), 404

@app.route("/api/sentiment", methods=["POST"])
def get_sentiment():
  data = request.get_json()
  artist = data.get("artist")
  song_name = data.get("song_name")
  song = genius.search_song(song_name, artist)
  if song is not None:
    raw_lyrics = song.lyrics
  else:
    return jsonify({"error": "Song not found"}), 404

  lines = raw_lyrics.split('\n')  # Split the lyrics into lines

  # Analyze sentiment for each line
  line_sentiments = []
  max_positive_line = {"line": "", "sentiment": {"compound": -1}}
  max_negative_line = {"line": "", "sentiment": {"compound": 1}}
  for line in lines:
    cleaned_line = clean_lyrics(line)
    preprocessed_line = preprocess_lyrics(cleaned_line)
    sentiment = analyze_sentiment(preprocessed_line)
    line_sentiments.append({"line": cleaned_line, "sentiment": sentiment})

    # Update most positive or most negative line if necessary
    if sentiment["compound"] > max_positive_line["sentiment"]["compound"]:
      max_positive_line = {"line": cleaned_line, "sentiment": sentiment}
    if sentiment["compound"] < max_negative_line["sentiment"]["compound"]:
      max_negative_line = {"line": cleaned_line, "sentiment": sentiment}

  return jsonify({"line_sentiments": line_sentiments, "max_positive_line": max_positive_line, "max_negative_line": max_negative_line})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  return app.send_static_file('index.html')

def preprocess_lyrics(lyrics: str):
  # Remove song structure tags or instructions in square brackets
  lyrics = re.sub(r'\[.*?\]', '', lyrics)
  
  # Remove unnecessary newlines
  lyrics = re.sub(r'\n', ' ', lyrics)
  
  # Remove punctuation and make lowercase
  lyrics = re.sub(r'[^\w\s]', '', lyrics).lower()

  # Tokenize and lemmatize the lyrics
  doc = nlp(lyrics)
  lemmatized_lyrics = " ".join([token.lemma_ for token in doc])
  
  # Remove stopwords
  cleaned_lyrics = " ".join(word for word in lemmatized_lyrics.split() if word not in stop_words)
  
  return cleaned_lyrics

def clean_lyrics(lyrics):
    cleaned_lyrics = re.sub(r'\[.*?\]', '', lyrics)  # Remove everything between square brackets
    cleaned_lyrics = re.sub(r'\{.*?\}', '', cleaned_lyrics)  # Remove everything between curly braces
    cleaned_lyrics = re.sub(r'\n{2,}', '\n', cleaned_lyrics)  # Remove excessive line breaks
    return cleaned_lyrics.strip()  # Remove leading and trailing whitespace

def analyze_sentiment(lyrics: str):
  sentiment = sia.polarity_scores(lyrics)
  return sentiment

if __name__ == "__main__":
  app.run()
