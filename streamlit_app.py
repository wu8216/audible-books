import streamlit as st
import pandas as pd
import locale

from views.search_video import show_contact_form, new_book_summary


# Load and cache the CSV content
@st.cache_data
def load_content():
    return pd.read_csv('data/tag_content.csv')

# Function to detect browser's language setting
def get_browser_language():
    lang_code = locale.getdefaultlocale()[0]
    return 'zh' if lang_code.startswith('zh') else 'en'

# Function to get content based on selected language
def get_content_by_language(content_df, lang):
    print("Available columns:", content_df.columns)  # Debugging line
    print("Selected language:", lang)  # Debugging line
    if lang not in content_df.columns:
        raise ValueError(f"Language column '{lang}' does not exist in the DataFrame")
    content_dict = dict(zip(content_df['tag'], content_df[lang]))
    return content_dict

# Load the CSV file
content_df = load_content()

# Set default language based on browser settings
default_language = get_browser_language()

# Language selection logic using query parameters
query_params = st.query_params
selected_language = query_params.get("lang", [default_language])[0]

# Get the content based on the selected language
content = st.session_state.get('content', {})
if not content:
    content = get_content_by_language(content_df, selected_language)

# Display the logo and language flags
st.logo("assets/audible_logo.png")

if st.sidebar.button(f"📚{content['newBookRequest']}"):
    show_contact_form(content)

if st.sidebar.button(f"📚{content.get('newRequestSummary', 'New Books List')}"):
    new_book_summary()

col1, col2 = st.sidebar.columns(2, gap="small", vertical_alignment="center")
with col1:
    if st.sidebar.button("🏳️‍🌈Change to English"):
        selected_language = 'en'
        content = get_content_by_language(content_df, selected_language)
        st.session_state.content = content
        st.session_state.language = selected_language

with col2:
    if st.sidebar.button("🚩切换中文"):
        selected_language = 'zh'
        content = get_content_by_language(content_df, selected_language)
        st.session_state.content = content
        st.session_state.language = selected_language

# --- PAGE SETUP ---
search_page = st.Page(
    "views/search_video.py",
    title=content['search'],  # Title in selected language
    icon="🔎",
    default=True,
)
project_1_page = st.Page(
    "views/AudibleBook.py",
    title=content['AudibleBook'],  # Title in selected language
    icon="⛪",
)
project_2_page = st.Page(
    "views/SjClassics.py",
    title=content['SJClassics'],  # Title in selected language
    icon="📚",
)
project_3_page = st.Page(
    "views/SpokenBooks.py",
    title=content['SpokenBooks'],  # Title in selected language
    icon="✝️",
)
project_4_page = st.Page(
    "views/WClassics.py",
    title=content['WClassics'],  # Title in selected language
    icon="📘",
)

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        content['search']: [search_page],
        content['channels']: [project_1_page, project_2_page, project_3_page, project_4_page],
    }
)

# --- RUN NAVIGATION ---
pg.run()

