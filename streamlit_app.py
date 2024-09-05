import streamlit as st


# --- PAGE SETUP ---
search_page = st.Page(
    "views/search_video.py",
    title="Search Videos (搜索视频)",
    icon="🔎",
    default=True,
)
project_1_page = st.Page(
    "views/AudibleBook.py",
    title="三位书屋",
    icon="⛪",
)
project_2_page = st.Page(
    "views/SjClassics.py",
    title="世界名著",
    icon="📚",
)
project_3_page = st.Page(
    "views/SpokenBooks.py",
    title="Christian Books",
    icon="✝️",
)
project_4_page = st.Page(
    "views/WClassics.py",
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
        "Search (搜索)": [search_page],
        "Channels (频道)": [project_1_page, project_2_page, project_3_page, project_4_page, project_5_page],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo("assets/audible_logo.png")
st.sidebar.markdown("Made with ❤️ by [Richard](https://www.linkedin.com/in/richard-wu-8988364/)")


# --- RUN NAVIGATION ---
pg.run()
