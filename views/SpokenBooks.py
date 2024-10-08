import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components
from streamlit_player import st_player

# Access the shared content
content = st.session_state.get('content', {})
language = st.session_state.get('language', 'en')

channel_name = 'SpokenBooks'
channel_display_name = content.get(channel_name, 'Christian Books')

# Create columns for the layout
col1, col2 = st.columns([1, 2])

# Column 1 for the image
with col1:
    st.image('assets/' + channel_name + '.jpg', width=200, caption=channel_display_name)

# Column 2 for the title and description
with col2:
    st.title(channel_display_name)
    st.write(content.get('scDescription', "This channel features a collection of Christian books from throughout history, presented as audiobooks to help people hear the message of Jesus Christ's salvation. It emphasizes the core truth that through faith in Jesus, hearts are transformed, sins are forgiven, and the gift of eternal life is granted to all who believe in Him."))

# @st.cache_data
def get_video_urls(file_type, column_name):
    # Reading the CSV file
    try:
        file_path = os.path.join(os.getcwd(), 'data', channel_name + file_type)
        file_df = pd.read_csv(file_path)

        # Sort the DataFrame in ascending order to display oldest first
        file_df_sorted = file_df.sort_values(by=column_name, ascending=False).reset_index(drop=False)
    except FileNotFoundError:
        st.error("The data file was not found.")
        st.stop()
    return file_df_sorted

recent_df_sorted = get_video_urls('_new.csv', "publishedAt")
pl_df_sorted = get_video_urls('_pl.csv', "Published At")

html = '''<iframe id="ytplayer" type="text/html" width="356" height="200"
src="https://www.youtube.com/embed/?listType=playlist&list={}"
frameborder="0" allowfullscreen></iframe>'''

# Pagination parameters
total_count = len(pl_df_sorted)
items_per_page = 10  # Total items per page
items_per_column = 5  # Items per column
columns_count = 2  # Number of columns

total_pages = (total_count - 1) // items_per_page + 1

# Using Markdown with inline CSS to style the text
st.markdown(
    f"""
    <style>
    .light-blue {{
        color: #ADD8E6; /* Light blue color */
    }}
    </style>
    <h2 class="light-blue">{content.get('recentTenVideos', "Most recent 10 audible books.")}</h1>
    """,
    unsafe_allow_html=True
)
# Create columns for layout
recent_cols = st.columns(columns_count)
for i in range(columns_count):
    with recent_cols[i]:
        for j in range(items_per_column):
            recent_index = i * items_per_column + j
            if recent_index < 10: # display 10 most recent only. len(recent_df_sorted)
                # Get the video URL and title
                recent_url = recent_df_sorted.at[recent_index, 'url']
                recent_name = recent_df_sorted.at[recent_index, 'title']

                # Display the video title and player
                st.write(recent_name)
                st_player(recent_url, height=200)
            else:
                break

# Using Markdown with inline CSS to style the text
st.markdown(
    f"""
    <style>
    .light-blue {{
        color: #ADD8E6; /* Light blue color */
    }}
    </style>
    <h2 class="light-blue">{content.get('playlist', "The full playlists, 10 playlists per page.")}</h1>
    """,
    unsafe_allow_html=True
)

# Get the current page number from the session state
if 'page' not in st.session_state:
    st.session_state.page = 1


def create_page_buttons(position):
    """Function to create pagination buttons with unique keys based on position"""
    cols = st.columns(total_pages)
    for i in range(total_pages):
        if cols[i].button(f"{i + 1}", key=f"{position}_page_{i + 1}"):
            st.session_state.page = i + 1


# Display pagination buttons at the top of the page
create_page_buttons('top')

# Display the items for the current page in a grid layout
start_idx = (st.session_state.page - 1) * items_per_page
end_idx = start_idx + items_per_page

# Create columns for layout
cols = st.columns(columns_count)

for i in range(columns_count):
    with cols[i]:
        for j in range(items_per_column):
            index = start_idx + i * items_per_column + j
            if index < total_count:
                url = "https://www.youtube.com/playlist?list=" + pl_df_sorted.at[index, 'Playlist ID']
                name = pl_df_sorted.at[index, 'Name']

                # Split the text if it contains a dash and format the text in one line
                if '-' in name:
                    name_parts = name.split('-', 1)
                    display_name = f'<a href="{url}" target="_blank" style="text-decoration: none; font-size: 20px;">{name_parts[0].strip()} - {name_parts[1].strip()}</a>'
                else:
                    display_name = f'<a href="{url}" target="_blank" style="text-decoration: none; font-size: 20px;">{name}</a>'

                # Display the subheader with the formatted name and larger font
                st.markdown(display_name, unsafe_allow_html=True)
                components.html(html.format(pl_df_sorted.at[index, 'Playlist ID']), width=356, height=200, scrolling=False)

# Display pagination buttons at the bottom of the page
create_page_buttons('bottom')

# Display the current page number
st.write(f"Page {st.session_state.page} of {total_pages}")