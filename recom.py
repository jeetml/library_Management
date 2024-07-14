import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Load your dataset (assuming you have a CSV file with book data)
@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

# Function to preprocess text data for TF-IDF vectorization
def preprocess_text(text):
    return str(text).lower()

# Function to get book recommendations based on user input
def get_recommendations(df, genres, authors, language, num_recommendations=5):
    try:
        # Filter books based on user input
        filtered_books = df[(df['genres'].str.contains(genres, case=False)) & 
                            (df['authors'].str.contains(authors, case=False)) & 
                            (df['language'].str.contains(language, case=False))]
        
        # If no books match the criteria
        if filtered_books.empty:
            return []
        
        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(filtered_books['title'].apply(preprocess_text))
        
        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # Get indices of top recommendations
        book_indices = sorted(list(enumerate(cosine_sim[0])), key=lambda x: x[1], reverse=True)[:num_recommendations]
        
        # Return recommended books
        recommendations = []
        for idx, _ in book_indices:
            recommendations.append(filtered_books.iloc[idx])
        
        return recommendations
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return []


# Main Streamlit app
def main():
    st.title('Book Recommendation System')
    
    # Load data
    file_path = 'bookfinal.csv'  # Update with your file path
    df = load_data(file_path)
    
    # Sidebar inputs
    st.sidebar.title('User Preferences')
    genres = st.sidebar.text_input('Enter Genre')
    authors = st.sidebar.text_input('Enter Author')
    language = st.sidebar.text_input('Enter Language')
    
    # Get recommendations based on user input
    recommendations = get_recommendations(df, genres, authors, language)
    
    # Display recommendations
    st.header('Top 5 Book Recommendations')
    for idx, book in enumerate(recommendations[:5]):  # Limiting to 5 recommendations
        st.subheader(f"Recommendation {idx + 1}")
        st.write(f"ISBN: {book['isbn']}")
        st.write(f"Title: {book['title']}")
        st.write(f"Series Title: {book['series_title']}")
        st.write(f"Series Release Number: {book['series_release_number']}")
        st.write(f"Author: {book['authors']}")
        st.write('---')

if __name__ == '__main__':
    main()
