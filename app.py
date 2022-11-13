import streamlit as st
import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

def fetch_poster(movie_id):
  response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, TMDB_API_KEY))


  # read json response
  data = response.json()
  # print(data)
  if not data['poster_path']:
    return "poster_not_found.png"
  else:
    return "https://image.tmdb.org/t/p/original" + data['poster_path']


def recommend(movie):
      #find the index of the movie 
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    
    #find distance between the input movie with other movies
    distance = similarity[movie_index]
    
    #find 5 recommended movies list
    recommended_list = sorted(list(enumerate(distance)), reverse = True, key = lambda x : x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in recommended_list:
        recommended_movies.append(movies_list.iloc[i[0]].title)

        #get the id of the movie
        movie_id = movies_list.iloc[i[0]].movie_id

        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
        # print(recommended_movies_posters)
        
    return recommended_movies, recommended_movies_posters


# Read back the list of movies
movies_list = pickle.load(open('movies.pkl', 'rb'))
# get only the tile of the movies
movies_title = movies_list['title'].values 

# Read back the similarity of movies
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Enter the Movie Name',
    movies_title)

if st.button('Find'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
      st.write(names[0])
      st.image(posters[0])
    with col2:
      st.write(names[1])
      st.image(posters[1])
    with col3:
      st.write(names[2])
      st.image(posters[2])
    with col4:
      st.write(names[3])
      st.image(posters[3])
    with col5:
      st.write(names[4])
      st.image(posters[4])

