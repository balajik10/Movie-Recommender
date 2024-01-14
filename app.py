import streamlit as st
import pickle
import pandas as pd
import requests

# Load the movie data and similarity matrix
movies_l = pickle.load(open('movies.pkl', 'rb'))
movies = movies_l['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movies_id):
   response=requests.get('http://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movies_id))
   data=response.json()
   return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

# Define the recommendation function
def recommend(movie):
    movie_index = movies_l[movies_l['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_poster=[]

    for i in movies_list:
        movies_id=movies_l.iloc[i[0]].movie_id
        recommended_movies.append(movies_l.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movies_id))



    # Move the return statement outside the loop
    return recommended_movies,recommended_movies_poster

# Streamlit app
st.title('Movie Recommender')

# Movie selection dropdown
selected_movie = st.selectbox('Which movie would you like to watch', movies)

# Recommend button
if st.button('Recommend'):
    names,posters = recommend(selected_movie)
    # for i in recommendations:
    #     st.write(i)
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
