import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from urllib.parse import urlencode

# Replace with your Google OAuth credentials
GOOGLE_CLIENT_ID = st.secrets["G_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["G_CLIENT_SECRET"]

# Define configuration
CLIENT_ID = GOOGLE_CLIENT_ID
CLIENT_SECRET = GOOGLE_CLIENT_SECRET
AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'
REDIRECT_URI = 'http://localhost:8501'
SCOPE = 'openid'

# Create OAuth2 session
oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)


# Function to show PDF page
def show_pdf_page():
    st.title('PDF Page')
    st.write('Content of the PDF page.')


# Function to show management page
def show_management_page():
    st.title('Management Page')
    st.write('Content of the management page.')


# Function to handle OAuth callback
def handle_oauth_callback():
    # Extract authorization code from the callback URL
    query_params = st.experimental_get_query_params()
    code = query_params.get('code', [None])[0]

    if code:
        try:
            # Exchange authorization code for access token
            token = oauth.fetch_token(
                TOKEN_ENDPOINT,
                authorization_response=f"{REDIRECT_URI}?code={code}",
                client_secret=CLIENT_SECRET
            )
            st.session_state['token'] = token
            st.session_state['authenticated'] = True
        except Exception as e:
            st.error(f"Failed to fetch token: {e}")
    else:
        st.error('Authorization code not found.')


# Display login button or handle callback
if 'token' not in st.session_state:
    # Step 1: Get authorization URL
    authorization_url, state = oauth.create_authorization_url(AUTHORIZATION_ENDPOINT)

    # Display login button
    if st.button('Login with Google'):
        st.write(f"[Click here to log in]({authorization_url})")

elif st.session_state.get('authenticated', False):
    # Display authenticated content
    st.sidebar.success('You are logged in!')

    # Page selection
    page = st.sidebar.radio('Select Page', ['Home', 'PDF', 'Management'])

    if page == 'PDF':
        show_pdf_page()
    elif page == 'Management':
        show_management_page()
    else:
        st.title('Home')
        st.write('Welcome to the home page.')
else:
    st.error('You are not authenticated. Please log in.')

# Handle OAuth callback
handle_oauth_callback()
