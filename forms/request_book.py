import re
import streamlit as st
import requests  # pip install requests
import pandas as pd
import os

# Retrieve webhook URL from Streamlit secrets
WEBHOOK_URL = st.secrets["WEBHOOK_URL"]

# Path to the CSV file
csv_file_path = 'data/user_request.csv'

# Ensure the CSV file exists, create it with headers if it does not
if not os.path.isfile(csv_file_path):
    df = pd.DataFrame(columns=['name', 'email', 'message'])
    df.to_csv(csv_file_path, index=False)


def is_valid_email(email):
    # Basic regex pattern for email validation
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None


def append_to_csv(name, email, message):
    # Append new data to the CSV file
    new_data = pd.DataFrame([[name, email, message]], columns=['name', 'email', 'message'])
    new_data.to_csv(csv_file_path, mode='a', header=False, index=False)


def new_book_summary_form():
    if not 'request_content' in st.session_state:
        st.text("No new book yet.")
    else:
        request_content = st.session_state.get('request_content', "No New Book Yet")
        st.text(request_content)


def book_request_form(content):
    # Create the contact form

    with st.form("book_request_form"):
        name = st.text_input(content.get("name", "Name"))
        email = st.text_input(content.get("emailAddress", "Email Address"))
        message = st.text_area(content.get("message", "New Book and Author Name"))
        submit_button = st.form_submit_button(content.get("submit", "Submit"))

    if submit_button:
        # Validate form fields
        if not WEBHOOK_URL:
            st.error(content.get("webhook_missing", "Email service is not set up. Please try again later."), icon="📧")
            st.stop()

        if not name:
            st.error(content.get("nameMissing", "Please provide your name."), icon="🧑")
            st.stop()

        if not email:
            st.error(content.get("emailAddressMissing", "Please provide your email address."), icon="📨")
            st.stop()

        if not is_valid_email(email):
            st.error(content.get("emailAddressInvalid", "Please provide a valid email address."), icon="📧")
            st.stop()

        if not message:
            st.error(content.get("messageMissing", "Please provide a book name and author."), icon="💬")
            st.stop()

        # Append data to CSV file
        append_to_csv(name, email, message)

        if 'request_content' in st.session_state:
            request_content = st.session_state['request_content']
        else:
            request_content = "name,requestDetail\n"

        # Append the new name and message
        request_content += f"{name},{message}\n"
        st.session_state['request_content'] = request_content

        # Prepare data payload for the webhook
        data = {"email": email, "name": name, "message": message}
        response = requests.post(WEBHOOK_URL, json=data)

        # Handle response from the webhook
        if response.status_code == 200:
            st.success(
                content.get("submitSuccess", "Your required book and author name have been sent successfully! 🎉"),
                icon="🚀")
        else:
            st.error(content.get("submitFailed", "There was an error sending your new book request."), icon="😨")

# Call the contact_form function to display the form
# contact_form()
