import streamlit as st
from pymongo import MongoClient
import hashlib

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["auth-diet"]
users_collection = db["auth-diet"]

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check login credentials
def check_login(username, password):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return True
    return False

# Signup function
def signup(username, password, email):
    if users_collection.find_one({"username": username}):
        st.error("Username already exists")
    else:
        users_collection.insert_one({
            "username": username,
            "password": hash_password(password),
            "email": email,  # Add email field
            "cart": []  # Initialize with an empty cart
        })
        st.success("Signup successful! Please log in.")

# Function to fetch user's details (for admin)
def get_user_info(username):
    user = users_collection.find_one({"username": username})
    if user:
        return {
            "username": user["username"],
            "email": user.get("email", ""),  # Handle case where email may be missing
            "cart": user.get("cart", [])  # Handle case where cart may be missing
        }
    else:
        return None

# Streamlit app layout
st.title("Book Recommendation System")

menu = ["Login", "Sign Up", "Profile", "Search Books", "Recommendation"]
choice = st.sidebar.selectbox("Menu", menu)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if st.session_state.logged_in:
    if st.session_state.username == "admin":
        st.write("<h1 style='text-align: center;'>Admin Panel</h1>", unsafe_allow_html=True)
        st.write("You have admin access.")
        st.header("Retrieve User Information")
        username_to_retrieve = st.text_input("Username to retrieve information")
        if st.button("Retrieve User Info"):
            if username_to_retrieve:
                user_info = get_user_info(username_to_retrieve)
                if user_info:
                    st.write("User Information:")
                    st.write(f"- Username: {user_info['username']}")
                    st.write(f"- Email: {user_info['email']}")
                    st.write("Cart:")
                    for item in user_info['cart']:
                        st.write(f"  - Title: {item['title']}, Price: ${item['price']}")
                else:
                    st.warning("Username not found")
            else:
                st.warning("Please enter a username")
    else:
        st.write(f"<h1 style='text-align: center;'>Welcome, {st.session_state.username}!</h1>", unsafe_allow_html=True)
        if choice == "Profile":
            import userp
            userp.main()
        elif choice == "Search Books":
            import search_books
            search_books.main()
        elif choice == "Recommendation":
            import recom
            recom.main()
else:
    if choice == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if check_login(username, password):
                st.success(f"Welcome {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password")

    elif choice == "Sign Up":
        st.subheader("Sign Up")

        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        new_email = st.text_input("Email")  # Add email input

        if st.button("Sign Up"):
            signup(new_username, new_password, new_email)
