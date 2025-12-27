import streamlit as st
import requests

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

def get_poster_url(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        response = requests.get(url).json()
        if response['results']:
            poster_path = response['results'][0]['poster_path']
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except: pass
    return "https://via.placeholder.com/500x750?text=No+Poster"

def render_recommendation_section(movies):
    # Creating a grid of clickable items
    cols = st.columns(len(movies))
    for i, (_, m) in enumerate(movies.iterrows()):
        with cols[i]:
            poster = get_poster_url(m['title'])
            # Image Display
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{poster}" style="width:100%; border-radius:15px;"/>
                    <div style="padding:10px; text-align:center;">
                        <p style="font-size:12px; font-weight:bold; color:white; margin:0;">{m['title']}</p>
                        <span style="color:#FFD700; font-size:10px;">★ {int(m['score']*100)}% Match</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Click to Expand Feature
            if st.button(f"View Info", key=f"btn_{m['title']}"):
                st.session_state.selected_from_rec = m['title']
                st.rerun()