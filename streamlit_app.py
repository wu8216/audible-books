import streamlit as st


# --- PAGE SETUP ---
about_page = st.Page(
    "views/about_me.py",
    title="About Us",
    icon=":material/account_circle:",
    default=True,
)
project_1_page = st.Page(
    "pages/AudibleBook.py",
    title="三位书屋",
    icon="⛪",
)
project_2_page = st.Page(
    "pages/SjClassics.py",
    title="世界名著",
    icon="📚",
)
project_3_page = st.Page(
    "pages/SpokenBooks.py",
    title="Christian Books",
    icon="✝️",
)
project_4_page = st.Page(
    "pages/WClassics.py",
    title="World Classics",
    icon="📘",
)
project_5_page = st.Page(
    "views/chatbot.py",
    title="Chat Bot",
    icon=":material/smart_toy:",
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [about_page],
        "Channels": [project_1_page, project_2_page, project_3_page, project_4_page, project_5_page],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo("assets/audible_logo.png")
st.sidebar.markdown("Made with ❤️ by [Richard](https://youtube.com/@audiblebook)")


# --- RUN NAVIGATION ---
pg.run()
