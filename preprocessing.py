import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def load_data(path="data/movies.csv"):
    """
    Load the movie dataset from CSV file.
    Replace missing genres & posters with defaults.
    """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Cannot find dataset at {path}")
    
    # Replace missing
    df['genres'] = df['genres'].fillna('')
    df['poster_url'] = df['poster_url'].replace('', np.nan)
    
    # For any missing posters use placeholder
    df['poster_url'].fillna("https://via.placeholder.com/200x300?text=No+Image", inplace=True)
    
    # Reset index explicitly
    df.reset_index(drop=True, inplace=True)
    return df

def vectorize_genres(df):
    """
    Turn combined genre text into a numerical genre matrix
    Useful for similarity computation.
    """
    # Get all genre tokens
    corpus = df['genres'].tolist()
    
    # Initialize count vectorizer
    cv = CountVectorizer(tokenizer=lambda x: x.split('|'), binary=True)
    genre_matrix = cv.fit_transform(corpus)
    
    # Debug prints for hackathon
    print(f"[INFO] Unique genres found: {len(cv.get_feature_names_out())}")
    print(f"[INFO] Genre features: {cv.get_feature_names_out()}")
    
    return genre_matrix
