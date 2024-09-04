import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

channel_name = 'AudiableBook'
channel_display_name = '三位书屋'

# Create columns for the layout
col1, col2 = st.columns([1, 2])

# Column 1 for the image
with col1:
    st.image('assets/' + channel_name + '.jpg', width=200, caption=channel_display_name)

# Column 2 for the title and description
with col2:
    st.title(channel_display_name)
    st.write("这个频道汇集了历史上的基督教书籍，并将其制作成有声读物，使人们更容易聆听，从而净化心灵，敬拜耶稣基督。任何信仰上帝的人都会获得永生。")

html = '''<iframe id="ytplayer" type="text/html" width="356" height="200"
src="https://www.youtube.com/embed/?listType=playlist&list={}"
frameborder="0" allowfullscreen></iframe>'''

# Reading the CSV file
try:
    path = os.path.join(os.getcwd(), 'data', channel_name + '_pl.csv')
    df = pd.read_csv(path)

    # Sort the DataFrame in ascending order to display oldest first
    df_sorted = df.sort_values(by="Published At", ascending=False).reset_index(drop=False)
except FileNotFoundError:
    st.error("The data file was not found.")
    st.stop()

# Pagination parameters
total_count = len(df_sorted)
items_per_page = 10  # Total items per page
items_per_column = 5  # Items per column
columns_count = 2  # Number of columns

total_pages = (total_count - 1) // items_per_page + 1

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
                url = "https://www.youtube.com/playlist?list=" + df_sorted.at[index, 'Playlist ID']
                name = df_sorted.at[index, 'Name']

                # Split the text if it contains a dash and format the text in one line
                if '-' in name:
                    name_parts = name.split('-', 1)
                    display_name = f'<a href="{url}" target="_blank" style="text-decoration: none; font-size: 20px;">{name_parts[0].strip()} - {name_parts[1].strip()}</a>'
                else:
                    display_name = f'<a href="{url}" target="_blank" style="text-decoration: none; font-size: 20px;">{name}</a>'

                # Display the subheader with the formatted name and larger font
                st.markdown(display_name, unsafe_allow_html=True)
                components.html(html.format(df_sorted.at[index, 'Playlist ID']), width=356, height=200, scrolling=False)

# Display the current page number
st.write(f"Page {st.session_state.page} of {total_pages}")

# Display pagination buttons at the bottom of the page
create_page_buttons('bottom')
