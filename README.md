# CineNexa - Movie Search App

A Streamlit app to search movies by title, genre, director, or keyword, displaying posters, ratings, and summaries.

## Features
- Search movies by multiple criteria including title, genre, and director.
- Displays movie posters fetched from TMDB API.
- Shows vote ratings and brief overview text.
- Keeps a list of recent search queries in the sidebar.
- Responsive design with 3 movies shown per row.

## Installation

1. Clone the repo:
   
2. Create and activate a Python environment (optional but recommended):

3. pip install -r requirements.txt

4. 
## Usage

Run the Streamlit app with:

streamlit run app.py


This will open the app in your default web browser.

## API Key

- You need a TMDB API key for movie posters. Replace the `TMDB_API_KEY` variable in `app.py` with your own key from [TMDB](https://www.themoviedb.org/documentation/api).

## License

This project is licensed under the MIT License.

## Acknowledgments

- Movie data and images powered by TMDB API.



Dataset and Data Processing Instructions
1. Extract Movie Data from TMDB API
Sign up and get your TMDB API Key from https://www.themoviedb.org/documentation/api

Use Python requests or tmdbv3api package to fetch movie metadata such as title, genres, overview, keywords, crew, ratings.


. Prepare DataFrame
Collect the fetched movie data into lists or dictionaries.

Convert to a Pandas DataFrame:

. Prepare DataFrame
Collect the fetched movie data into lists or dictionaries.

Convert to a Pandas DataFrame:
Save Data as Pickle Files
Save the DataFrame as a pickle file for faster loading in the app:

df.to_pickle('movie_full_dict.pkl')

If you have a similarity matrix (for recommendations), save it similarly:

 Load Data in App
In your Streamlit app, load the pickle files:


import pickle

movie_dict = pickle.load(open('movie_full_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))





