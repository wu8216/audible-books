import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

# Use the app-specific password here
gmail_user = st.secrets["G_USER"]
gmail_password = st.secrets["G_PWD"]

def send_email(to_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.quit()
        st.success(f"Email successfully sent to {to_email}")
    except Exception as e:
        st.error(f"Failed to send email. Error: {str(e)}")

# Streamlit UI
st.title("Send an Email using Gmail")

to_email = st.text_input("Recipient Email")
subject = st.text_input("Email Subject")
message = st.text_area("Email Message")

if st.button("Send Email"):
    if to_email and subject and message:
        send_email(to_email, subject, message)
    else:
        st.error("Please fill in all fields")
