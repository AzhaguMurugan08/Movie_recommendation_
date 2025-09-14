# CineNexa  
A Streamlit app to search movies by title, genre, director, or keyword, displaying posters, ratings, and summaries.

## Features
- Search movies by multiple criteria including title, genre, and director.
- Displays movie posters fetched from TMDB API.
- Shows vote ratings and brief overview text.
- Keeps a list of recent search queries in the sidebar.
- Responsive design with 3 movies shown per row.

## Installation
1. Clone the repo:
 git clone https://github.com/your-username/cinenexa.git](https://github.com/AzhaguMurugan08/Movie_recommendation_


3. Install the required dependencies:


## Usage
Run the Streamlit app with:




This will open the app in your default web browser.

## API Key
You need a TMDB API key for movie posters. Replace the `TMDB_API_KEY` variable in `app.py` with your own key from [TMDB](https://www.themoviedb.org/documentation/api).

## Dataset and Data Processing Instructions

### Extract Movie Data from TMDB API
- Sign up and get your TMDB API Key from [TMDB API](https://www.themoviedb.org/documentation/api).
- Use Python requests or `tmdbv3api` package to fetch movie metadata such as title, genres, overview, keywords, crew, and ratings.
- Sample code to fetch movie data:

import requests

API_KEY = "your_api_key"
movie_id = 550

url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
response = requests.get(url)
data = response.json()
print(data['title'], data['genres'], data['overview'])


### Prepare DataFrame
- Collect fetched movie data into dictionaries or lists.
- Convert data into a Pandas DataFrame:

import pandas as pd

movies_data = [
{"title": "Inception", "genres": ["Action", "Sci-Fi"], "overview": ".

..", "crew": "Christopher Nolan", "vote_average": 8.8},
# Add more movies here
]

df = pd.DataFrame(movies_data)




### Save Data as Pickle Files
- Save the DataFrame as a pickle file for efficient loading in the app:


df.to_pickle('movie_full_dict.pkl')



import pickle
similarity_matrix = ... # your similarity matrix
with open('similarity.pkl', 'wb') as f:
pickle.dump(similarity_matrix, f)


### Load Data in App
- Load pickle files in your Streamlit app:

import pickle

movie_dict = pickle.load(open('movie_full_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))



## License
This project is licensed under the MIT License.

## Acknowledgments
- Movie data and images powered by TMDB API.


