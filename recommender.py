

# import pandas as pd
# import requests

# API_KEY = ''

# def fetch_poster(movie_title):
#     url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
#     response = requests.get(url).json()
#     if response['results']:
#         poster_path = response['results'][0].get('poster_path')
#         if poster_path:
#             return f"https://image.tmdb.org/t/p/w500{poster_path}"
#     return "https://via.placeholder.com/200x300?text=No+Image"

# def recommend_movies_with_posters(movie_title, top_n=5):
#     from sklearn.feature_extraction.text import TfidfVectorizer
#     from sklearn.metrics.pairwise import cosine_similarity

#     movies = pd.read_csv('movies.csv')
#     movies['genre'] = movies['genre'].fillna('')

#     vectorizer = TfidfVectorizer(token_pattern=r'[^|]+')
#     genre_matrix = vectorizer.fit_transform(movies['genre'])
#     similarity = cosine_similarity(genre_matrix)

#     if movie_title not in movies['title'].values:
#         return []

#     idx = movies[movies['title'] == movie_title].index[0]
#     scores = list(enumerate(similarity[idx]))
#     scores = sorted(scores, key=lambda x: x[1], reverse=True)
#     top_movies = [movies.iloc[i[0]]['title'] for i in scores[1:top_n+1]]

#     return [{'title': title, 'poster': fetch_poster(title)} for title in top_movies]


import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = "Your TMDB Key Here Get It From https://www.themoviedb.org/signup"  # Replace with your TMDB key

def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    response = requests.get(url).json()
    if response['results']:
        poster_path = response['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/200x300?text=No+Image"

def recommend_movies_with_posters(movie_title, top_n=5):
    movies = pd.read_csv('movies.csv')
    movies.columns = movies.columns.str.strip()
    movies['genre'] = movies['genre'].fillna('')
    movies['title_lower'] = movies['title'].str.lower()

    movie_title_input = movie_title.strip().lower()
    print("User typed:", movie_title_input)
    print("Available titles:", movies['title_lower'].tolist())

    if movie_title_input not in movies['title_lower'].values:
        print("Movie not found in dataset")
        return []

    idx = movies[movies['title_lower'] == movie_title_input].index[0]

    # Compute similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    vectorizer = TfidfVectorizer(token_pattern=r'[^|]+')
    genre_matrix = vectorizer.fit_transform(movies['genre'])
    similarity = cosine_similarity(genre_matrix)

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in scores[1:top_n+1]:
        title = movies.iloc[i[0]]['title']
        poster = fetch_poster(title)
        recommendations.append({'title': title, 'poster': poster})

    return recommendations

