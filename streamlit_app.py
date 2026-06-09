import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Load data
@st.cache_resource
def load_data():
    try:
        with open("movie_data.pkl", "rb") as f:
            movies = pickle.load(f)

        with open("similarity_matrix.pkl", "rb") as f:
            similarity = pickle.load(f)

        similarity = np.array(similarity)

        return movies, similarity, None

    except Exception as e:
        return None, None, str(e)

new_df, similarity, error = load_data()

if error:
    st.error(f"Error loading files: {error}")
    st.stop()

# Recommendation function
def recommend(movie_title):
    try:
        movie_index = new_df[
            new_df["title"].str.lower() == movie_title.lower()
        ].index[0]

        distances = similarity[movie_index]

        movies_list = sorted(
            list(enumerate(distances)),
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = []

        for movie in movies_list[1:6]:
            recommendations.append(
                new_df.iloc[movie[0]]["title"]
            )

        return recommendations

    except Exception as e:
        return [f"Error: {e}"]

# UI
st.title("🎬 Movie Recommendation System")

st.write("Select a movie and get similar movie recommendations.")

movie_list = sorted(new_df["title"].tolist())

selected_movie = st.selectbox(
    "Choose a movie",
    movie_list
)

if st.button("Show Recommendations"):

    recommendations = recommend(selected_movie)

    st.subheader(f"Movies similar to '{selected_movie}'")

    for i, movie in enumerate(recommendations, start=1):
        st.write(f"**{i}.** {movie}")

st.markdown("---")
st.caption("Built using Streamlit")
