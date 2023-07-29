import pickle

import pandas as pd
import streamlit as st
import requests

df = pd.read_pickle('movies.pkl')

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2d750486af1f95628d06726fc1e36f4a&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list1 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_name = []
    recommended_movies_posters=[]

    for i in movies_list1:
        movie_id=df.iloc[i[0]].movie_id

        recommended_movies_name.append(df.iloc[i[0]].title)
        # fetch movie poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies_name,recommended_movies_posters


similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_list['title'].values
st.title('Movie Recommendation System')
print(movies_list)
selected_movie_name = st.selectbox(
    'Select a movie',
    movies_list)
if st.button('Recommend'):
    recommended_movies_name, recommended_movies_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_posters[1])
    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_posters[4])


