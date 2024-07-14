import streamlit as st
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId for MongoDB's _id
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["auth-diet"]
users_collection = db["auth-diet"]

# Email configuration for Gmail SMTP server
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USERNAME = "urvpatelhitack313@gmail.com"  # Replace with your Gmail address
EMAIL_PASSWORD = "bhtchsfsiaugrmps"  # Replace with your app-specific password
# receiver_email = "jeetnoad123@gmail.com"
def fetch_user_data(username):
    user = users_collection.find_one({"username": username})
    return user

def fetch_user_books(username):
    user = users_collection.find_one({"username": username})
    if user and "cart" in user:
        return user["cart"]
    return []

def delete_book_from_cart(username, book_title):
    # Update document in MongoDB to pull the specified book by its title
    users_collection.update_one(
        {"username": username},
        {"$pull": {"cart": {"title": book_title}}}
    )

def calculate_total_price(user_books):
    total_price = sum(book['price'] for book in user_books)
    return total_price

def calculate_days_remaining(return_date):
    # Calculate days remaining from today to return_date
    return_date = datetime.strptime(return_date, "%Y-%m-%d")
    today = datetime.now()
    remaining_days = (return_date - today).days
    return remaining_days, remaining_days <= 10  # Return days remaining and flag for alert

def send_email_alert(receiver_email, book_title):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = receiver_email
    msg['Subject'] = "Book Return Alert"

    body = f"Reminder: The book '{book_title}' borrowed from your cart is due in 10 days. Please make arrangements to return it."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USERNAME, receiver_email, text)
        server.quit()
        st.success(f"Email alert sent for book: '{book_title}'")
    except Exception as e:
        st.error(f"Failed to send email alert: {str(e)}")

def main():
    st.title("User Profile")

    username = st.session_state.username
    user_data = fetch_user_data(username)
    user_books = fetch_user_books(username)

    st.subheader(f"Welcome {username}!")

    st.write("### Your Profile Information")
    st.write(f"Username: {user_data['username']}")

    st.write("### Your Book Cart")
    if user_books:
        total_price = calculate_total_price(user_books)
        st.write(f"Total Price: ${total_price:.2f}")
        for book in user_books:
            st.write(f"- {book['title']} (${book['price']})")
            if 'borrowed_date' in book and 'return_date' in book:
                days_remaining, alert_flag = calculate_days_remaining(book['return_date'])
                if days_remaining >= 0:
                    st.write(f"   - Borrowed until: {book['return_date']} ({days_remaining} days remaining)")
                    if alert_flag:
                        st.write(f"      - Alert: You will receive an email when 10 days are left")
                        # Check if it's time to send an alert email
                        if days_remaining <= 10:
                            if 'email' in user_data:
                                send_email_alert(user_data['email'], book['title'])
                            else:
                                st.error("No email address provided. Please update your profile with an email address.")
                else:
                    st.write(f"   - Borrowed until: {book['return_date']} (Expired)")
            # Add a delete button for each book
            if st.button(f"Delete {book['title']}"):
                delete_book_from_cart(username, book['title'])
                st.experimental_rerun()  # Refresh the page after deletion
    else:
        st.write("Your cart is empty.")

    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

if __name__ == "__main__":
    main()
