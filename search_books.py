import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["auth-diet"]
users_collection = db["auth-diet"]

# Load books data
def load_books_data():
    books_df = pd.read_csv('bookfinal.csv')
    return books_df

def add_book_to_user(username, book, borrow_period=30):
    user = users_collection.find_one({"username": username})
    if user:
        if "cart" not in user:
            user["cart"] = []
        # Calculate return date
        return_date = datetime.now() + timedelta(days=borrow_period)
        user["cart"].append({
            "title": book['title'],
            "price": book['price'],
            "borrowed_date": datetime.now().strftime("%Y-%m-%d"),
            "return_date": return_date.strftime("%Y-%m-%d")
        })
        users_collection.update_one({"username": username}, {"$set": {"cart": user["cart"]}})
        st.success(f"Book '{book['title']}' added to your cart for borrowing until {return_date.strftime('%Y-%m-%d')}!")

def main():
    st.title("Search Books")

    books_df = load_books_data()
    search_query = st.text_input("Search for books")

    if search_query:
        results = books_df[books_df['title'].str.contains(search_query, case=False, na=False)]
        
        for index, row in results.iterrows():
            st.image("default_img.jpg", width=100)  # Add default image
            st.write(f"**Title:** {row['title']}")
            st.write(f"**Author:** {row['authors']}")
            st.write(f"**Publisher:** {row['publisher']}")
            if st.button(f"More Info: {row['title']}", key=row['isbn']):
                st.write(f"**Series Title:** {row['series_title']}")
                st.write(f"**Series Release Number:** {row['series_release_number']}")
                st.write(f"**Language:** {row['language']}")
                st.write(f"**Description:** {row['description']}")
                st.write(f"**Number of Pages:** {row['num_pages']}")
                st.write(f"**Format:** {row['format']}")
                # st.write(f"**Genres:** {row['genres']}")
                st.write(f"**Publication Date:** {row['publication_date']}")
                st.write(f"**Rating Score:** {row['rating_score']}")
                st.write(f"**Price:** {row['price']}")
                st.write(f"**URL:** {row['url']}")
            
            if st.button(f"Add to Cart: {row['title']}", key="add_" + row['isbn']):
                add_book_to_user(st.session_state.username, row)

            if st.button(f"Borrow: {row['title']}", key="borrow_" + row['isbn']):
                add_book_to_user(st.session_state.username, row, borrow_period=30)

if __name__ == "__main__":
    main()
