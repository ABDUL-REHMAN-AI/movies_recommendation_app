import streamlit as st

def display_recommendations(similar_movies):
    st.subheader("🎬 Recommended Movies:")
    cols = st.columns(3)
    for i, (_, row) in enumerate(similar_movies.iterrows()):
        col = cols[i % 3]
        col.image(row['poster_url'], use_column_width=True)
        col.markdown(f"**{row['title']}**")
        col.markdown(f"*Genres:* {row['genres']}")
        col.markdown(f"*Similarity:* {row['score']:.2f}")
