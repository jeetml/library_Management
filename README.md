# Library Managment System

This Streamlit application allows users to search for books, add them to their cart, and receive personalized book recommendations. The application also supports user authentication, profile management, and an admin panel for managing user information.

## Features

- **User Authentication**: Users can sign up and log in using their credentials.
- **Profile Management**: Users can view and manage their profile information.
- **Search Books**: Users can search for books and view detailed information about each book.
- **Book Cart**: Users can add books to their cart and view the total price of the books in their cart.
- **Recommendations**: Users can receive personalized book recommendations.
- **Admin Panel**: Admins can retrieve information about any user and view their cart.

## Email Alert Functionality

The application includes an email alert system to notify users when a borrowed book is due in 10 days. This feature helps users remember to return books on time. Here’s a brief explanation of how it works:

1. **Borrowing a Book**: When a book is borrowed, the return date is set to 30 days later.
2. **Calculating Remaining Days**: The application calculates the number of days remaining until the return date.
3. **Sending Alerts**: If there are 10 days left, the application sends an email reminder to the user's email address provided during sign-up. This is handled using Python's `smtplib` and `email` modules.
## Usage

### Sign Up

1. Open the application.
2. Select "Sign Up" from the sidebar menu.
3. Enter a new username, password, and email address.
4. Click "Sign Up" to create a new account.

### Log In

1. Open the application.
2. Select "Login" from the sidebar menu.
3. Enter your username and password.
4. Click "Login" to access your account.

### Profile Management

1. Log in to your account.
2. Select "Profile" from the sidebar menu.
3. View and manage your profile information, including the list of books in your cart.

### Search Books

1. Log in to your account.
2. Select "Search Books" from the sidebar menu.
3. Enter a search query to find books.
4. View detailed information about each book and add books to your cart.

### Recommendations

1. Log in to your account.
2. Select "Recommendation" from the sidebar menu.
3. Receive personalized book recommendations based on your profile.

### Admin Panel

1. Log in to your admin account.
2. Select "Admin Panel" from the sidebar menu.
3. Retrieve information about any user and view their cart.
