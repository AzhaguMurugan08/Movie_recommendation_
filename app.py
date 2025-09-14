import streamlit as st
import pickle
import pandas as pd
import requests
from math import ceil

# --- Set wide page layout ---
st.set_page_config(layout="wide")

# --- CONFIG ---
TMDB_API_KEY = "984d36210343a65f36575936800dbc5e"

def fetch_poster(movie_title):
    """Fetch poster URL from TMDB API for a given movie title."""
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
        response = requests.get(url)
        data = response.json()
        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass
    return "https://via.placeholder.com/350x525?text=No+Poster"

# --- LOAD DATA ---
movie_dict = pickle.load(open('movie_full_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
movies['genres'] = movies['genres'].apply(lambda x: x.split() if isinstance(x, str) else x)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- GLOBAL CSS ---
st.markdown(
    """
    <style>
    /* Main background */
    .main .block-container {
        padding: 48px 48px 48px 48px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 80%);
        min-height: 100vh;
    }
    body, .css-1d391kg, .css-1v3fvcr {
        font-size: 20px !important;
        line-height: 1.7 !important;
        color: #cbd5e1 !important;
    }

    /* Header */
    h1 {
        font-weight: 800 !important;
        text-align: center !important;
        color: #60a5fa !important;
        margin-top: 40px !important;
        margin-bottom: 30px !important;
        font-size: 68px !important;
    }
    h1 > span {
        font-size: 80px !important;
        vertical-align: middle;
        margin-right: 12px;
    }

    /* Smaller search box */
    div[data-baseweb="input"] > input {
        height: 50px !important;
        font-size: 20px !important;
        padding-left: 14px !important;
        width: 80% !important;     /* reduced width */
        max-width: 500px !important;
        margin: 0 auto 30px auto !important;
        display: block !important;
        border-radius: 10px !important;
        border: 2px solid #60a5fa !important;
        background-color: #0f172a !important;
        color: #cbd5e1 !important;
    }
    div[data-baseweb="input"] > input::placeholder {
        color: #64748b !important;
    }

    /* Sidebar black + grey */
    section[data-testid="stSidebar"] {
        background-color: #000 !important;
    }
    [data-testid="stSidebar"] * {
        color: #d1d5db !important;
    }
    .history-box {
        background-color: #111827;
        color: #d1d5db;
        border-radius: 10px;
        padding: 16px;
        max-height: 280px;
        overflow-y: auto;
        font-size: 16px;
    }

    /* Movie card adjustments */
    .movie-card {
        text-align: center;
        background: #1e293b;
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 24px;
        min-height: 550px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        box-shadow: 0 0 10px rgb(96 165 250 / 0.5);
        transition: transform 0.2s ease-in-out;
    }
    .movie-card:hover {
        transform: scale(1.04);
        box-shadow: 0 0 22px rgb(96 165 250 / 0.7);
    }
    .movie-poster {
        border-radius: 10px;
        width: 280px;
        margin: 0 auto 15px auto;
        flex-shrink: 0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.6);
    }
    .movie-title {
        font-size: 22px;
        font-weight: 700;
        color: white;
        margin: 10px 0;
    }
    .movie-meta {
        font-size: 16px;
        color: #60a5fa;
        margin-bottom: 12px;
    }
    .movie-overview {
        font-size: 16px;
        color: #cbd5e1;
        text-align: justify;
        flex-grow: 1;
    }

    /* Button styling */
    div.stButton > button {
        background-color: #2563eb;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin: 0 auto 40px auto;
        display: block;
    }
    div.stButton > button:hover {
        background-color: #1e40af;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- HEADER ---
st.markdown(
    """
    <h1><span>🍿</span>CineNexa</h1>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR ---
st.sidebar.markdown("<h3>📜 Recent Searches</h3>", unsafe_allow_html=True)

if st.session_state.history:
    history_html = "<div class='history-box'>"
    for term in reversed(st.session_state.history[-5:]):
        history_html += f"• {term}<br>"
    history_html += "</div>"
else:
    history_html = "<div class='history-box'>No search history yet.</div>"
st.sidebar.markdown(history_html, unsafe_allow_html=True)

# --- SEARCH BAR ---
search_query = st.text_input("🔎 Search by Movie Title, Genre, Director, or Keyword:")

if st.button("Search"):
    query = search_query.strip().lower()
    if not query:
        st.warning("⚠️ Please enter a search term.")
    else:
        st.session_state.history.append(search_query)

        matched_movies = movies[
            movies['title'].str.lower().str.contains(query, na=False) |
            movies['overview'].str.lower().str.contains(query, na=False) |
            movies['keywords'].str.lower().str.contains(query, na=False) |
            movies['genres'].apply(lambda g: any(query in x.lower() for x in (g if isinstance(g, list) else []))) |
            movies['crew'].str.lower().str.contains(query, na=False)
        ]

        if matched_movies.empty:
            st.error("❌ No movies matched your search.")
        else:
            st.markdown("<h3 style='color:#3b82f6;'>🎬 Search Results</h3>", unsafe_allow_html=True)

            matches = matched_movies.to_dict(orient='records')
            num_per_row = 3   # show 3 movies per row
            num_rows = ceil(len(matches) / num_per_row)

            for row_idx in range(num_rows):
                cols = st.columns(num_per_row, gap="large")
                for col_idx in range(num_per_row):
                    idx = row_idx * num_per_row + col_idx
                    if idx >= len(matches):
                        break
                    movie = matches[idx]
                    poster_url = fetch_poster(movie['title'])

                    with cols[col_idx]:
                        overview_text = movie['overview'] if pd.notna(movie['overview']) else "No overview available."
                        if len(overview_text) > 250:
                            overview_text = overview_text[:247] + "..."

                        st.markdown(
                            f"""
                            <div class="movie-card">
                                <img src="{poster_url}" class="movie-poster">
                                <p class="movie-title">{movie['title']}</p>
                                <p class="movie-meta">⭐ {movie['vote_average']} | 🎬 {movie['crew']}</p>
                                <p class="movie-overview">{overview_text}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
