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

def contact_form():
    # Create the contact form
    with st.form("contact_form"):
        name = st.text_input("Name (名字)")
        email = st.text_input("Email Address （电子邮件地址）")
        message = st.text_area("Request Book and Author Name (请求书名和作者名)")
        submit_button = st.form_submit_button("Submit （提交）")

    if submit_button:
        # Validate form fields
        if not WEBHOOK_URL:
            st.error("Email service is not set up. Please try again later.", icon="📧")
            st.stop()

        if not name:
            st.error("Please provide your name.", icon="🧑")
            st.stop()

        if not email:
            st.error("Please provide your email address.", icon="📨")
            st.stop()

        if not is_valid_email(email):
            st.error("Please provide a valid email address.", icon="📧")
            st.stop()

        if not message:
            st.error("Please provide a message.", icon="💬")
            st.stop()

        # Append data to CSV file
        append_to_csv(name, email, message)

        # Prepare data payload for the webhook
        data = {"email": email, "name": name, "message": message}
        response = requests.post(WEBHOOK_URL, json=data)

        # Handle response from the webhook
        if response.status_code == 200:
            st.success("Your message has been sent successfully! 🎉", icon="🚀")
        else:
            st.error("There was an error sending your message.", icon="😨")

# Call the contact_form function to display the form
# contact_form()
