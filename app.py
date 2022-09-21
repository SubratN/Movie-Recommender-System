import streamlit as st
import pickle
import pandas as pd
import requests

movies_list = pickle.load(open('model\movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('model\similarity.pkl','rb'))


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2eaaf09e02f945b75eed66df185a3a2c&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])),reverse=True, key = lambda x: x[1])

    recommended_movies = []
    recommended_movies_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch movie names
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch movie poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'Please Select Your Movie...',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])