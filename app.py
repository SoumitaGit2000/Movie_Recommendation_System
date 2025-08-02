import pickle
import streamlit as st
import pandas as pd
import requests

movie = pickle.load(open('movies_dictionary.pkl','rb'))
movie_df = pd.DataFrame(movie)

similarity = pickle.load(open('similarity.pkl','wb'))

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=fdbe560f08500df98a5c44074d4d1d1c')
    data = response.json()
    # poster = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    # return 'https://image.tmdb.org/t/p/original/' + data['poster_path']


def recommend(movie):
    if movie not in movie_df['original_title'].values:
        return ["Movie not found in the dataset."]

    movie_index = movie_df[movie_df['original_title'] == movie].index[0]
    distence = similarity[movie_index]
    movie_list = sorted(list(enumerate(distence)), reverse=True, key=lambda x: x[1])[1:6]

    reco_list = []
    reco_poster = []

    for i in movie_list:
        movie_id = movie_df.iloc[i[0]].id # fetching movie id
        reco_list.append(movie_df.iloc[i[0]].original_title)
        reco_poster.append(fetch_poster(movie_id)) # fetching poster
    return reco_list,reco_poster



st.title("Movie Recommender System")

selected_movie = st.selectbox(
    "Choose a movie:",
    movie_df['original_title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

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

