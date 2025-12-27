from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def get_similar_movies(title, df, genre_matrix, top_n=5):
    """
    Returns a DataFrame with movies similar to a given title
    based on cosine similarity of genre vectors.
    """
    # Validate title
    if title not in df['title'].values:
        print(f"[WARN] '{title}' not in database — returning empty.")
        return pd.DataFrame(columns=['title','genres','poster_url','score'])
    
    # Find index
    idx = df[df['title'] == title].index[0]
    
    # Compute similarity
    sim_scores = cosine_similarity(genre_matrix[idx], genre_matrix).flatten()
    
    # Sort and take top_n (excluding itself)
    sim_indices = sim_scores.argsort()[-(top_n+1):][::-1]
    sim_indices = [i for i in sim_indices if i != idx][:top_n]
    
    # Prepare similar
    recs = df.iloc[sim_indices].copy()
    recs['score'] = sim_scores[sim_indices]
    
    # Guarantee no missing posters
    recs['poster_url'] = recs['poster_url'].replace('', "https://via.placeholder.com/200x300?text=No+Image")
    
    return recs[['title','genres','poster_url','score']]
