# LyricLens

<p align="center">
  <img src="lyriclens.jpg" alt="LyricLens Logo" width="200">
</p>

LyricLens is a music sentiment analysis tool that leverages Natural Language Processing (NLP) techniques and machine learning models to determine the sentiment of song lyrics. 

## Overview

LyricLens uses the Spotify and Genius APIs to fetch song details and lyrics. It preprocesses the lyrics using NLTK and SpaCy and then applies a fine-tuned sentiment analysis model to predict the overall sentiment of the lyrics. The model's prediction can range from very negative to very positive, providing insight into the emotional tone of the song.

## Features

- Fetch song lyrics using Spotify and Genius APIs
- Preprocess lyrics for sentiment analysis
- Apply a fine-tuned sentiment analysis model to lyrics
- Deploy a machine learning model using Flask/FastAPI
- Provide an interactive front-end for users to input a song and receive its sentiment analysis
- Include testing and a CI/CD pipeline for robust development

## Future Work

- Extend the sentiment analysis model to detect more nuanced emotions in lyrics
- Improve the front-end with a more detailed analysis and better user experience
- Scale the application to support a larger number of concurrent users

## Author

Sam Groenjes - Initial work

## License

This project is licensed under the MIT License
