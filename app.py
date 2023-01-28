import streamlit as slt
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=03c2d7e377556f8bf80642f566eed214&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
df = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


def recommend(movies):
    movie_index = df[df['title'] == movies].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    suggested_movies = []
    suggested_movies_poster =[]
    for i in movies_list:
        movie_id = df.iloc[i[0]].movie_id
        suggested_movies.append(df.iloc[i[0]].title)
        suggested_movies_poster.append(fetch_poster(movie_id))
    return suggested_movies, suggested_movies_poster

slt.title('Movie Recommedation Page')

selected_movie_name = slt.selectbox(
    'Select the movie',
    df['title'].values
)
if slt.button('recommend'):
    suggestions ,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = slt.columns(5)

    with col1:
        slt.text(suggestions[0])
        slt.image(posters[0])

    with col2:
        slt.text(suggestions[1])
        slt.image(posters[1])

    with col3:
        slt.text(suggestions[2])
        slt.image(posters[2])
    with col4:
        slt.text(suggestions[3])
        slt.image(posters[3])
    with col5:
        slt.text(suggestions[4])
        slt.image(posters[4])
