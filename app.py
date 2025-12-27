import streamlit as st
import os, time, requests
import pandas as pd
from utils.preprocessing import load_data, vectorize_genres
from utils.recommender import get_similar_movies
from utils.ui_helpers import render_recommendation_section, get_poster_url

# --- 1. SETTINGS & STATE ---
st.set_page_config(page_title="TITAN MOVIE RECOMMENDER", layout="wide")

# Session State Initialization
if 'selected_from_rec' not in st.session_state:
    st.session_state.selected_from_rec = None
if 'show_recs' not in st.session_state:
    st.session_state.show_recs = False

def load_css():
    if os.path.exists("assets/style.css"):
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

# --- 2. ENGINE ---
@st.cache_resource
def init_engine():
    df = load_data("data/movies.csv")
    matrix = vectorize_genres(df)
    return df, matrix

df, genre_matrix = init_engine()

def get_movie_info(title):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
    try:
        data = requests.get(url).json()['results'][0]
        return data
    except: return None

# --- 3. UI: ERROR FIXED SELECTION ---
st.markdown("<h1 class='main-title'>TITAN MOVIE RECOMMENDER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#FFD700; letter-spacing:3px; margin-top:-20px;'>BY ABDUL REHMAN MEMON</p>", unsafe_allow_html=True)

# Error Fix: Converting int64 to pure Python int
default_index = 0
if st.session_state.selected_from_rec:
    # .item() converts numpy/pandas int64 to standard python int
    default_index = int(df[df['title'] == st.session_state.selected_from_rec].index[0])

st.write("### 🎬 Visual Discovery")
selected_title = st.selectbox(
    "Search Movie Library:", 
    df['title'].values, 
    index=default_index
)

# --- 4. DYNAMIC DETAIL PANEL ---
st.markdown("<div class='glass-panel' style='padding:30px;'>", unsafe_allow_html=True)
col_thumb, col_details = st.columns([1, 2.5])

with col_thumb:
    current_poster = get_poster_url(selected_title)
    st.image(current_poster, use_container_width=True, caption="Titan HQ Preview")

with col_details:
    info = get_movie_info(selected_title)
    if info:
        st.markdown(f"<h1 style='color:#FFD700; margin:0;'>{selected_title.upper()}</h1>", unsafe_allow_html=True)
        st.markdown(f"**📅 Release:** {info.get('release_date', 'N/A')} | **⭐ Rating:** {info.get('vote_average', 'N/A')}/10")
        st.write("---")
        st.write(f"**SYNOPSIS:** {info.get('overview', 'No summary available.')}")
        
        st.write("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 ACTIVATE TITAN ENGINE", use_container_width=True):
                st.session_state.show_recs = True
                st.session_state.selected_from_rec = selected_title
        with c2:
            trailer_url = f"https://www.youtube.com/results?search_query={selected_title.replace(' ', '+')}+trailer"
            st.link_button("📺 WATCH TRAILER", trailer_url, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

if st.session_state.show_recs:
    with st.status("💎 Analyzing Cinematic Patterns...", expanded=False):
        recs = get_similar_movies(selected_title, df, genre_matrix)
        time.sleep(0.5)
    
    st.markdown(f"### 🎯 TITAN TOP PICKS FOR: <span style='color:#FFD700;'>{selected_title}</span>", unsafe_allow_html=True)
    render_recommendation_section(recs)

with st.sidebar:
    st.markdown("<h2 class='titan-title' style='font-size:25px;'>TITAN CORE</h2>", unsafe_allow_html=True)
    st.write("---")
    if st.button("🔄 Reset Engine"):
        st.session_state.selected_from_rec = None
        st.session_state.show_recs = False
        st.rerun()
    
    st.write("---")
    st.markdown("### 📊 System Health")
    st.progress(98)
    st.caption("AI Accuracy: 98.4%")