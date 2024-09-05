from forms.request_book import book_request_form, new_book_summary_form
import streamlit as st
import pandas as pd
from streamlit_player import st_player

# Access the shared content
content = st.session_state.get('content', {})
language = st.session_state.get('language', 'en')
dialog_title = content.get('bookRequest', 'New Book Request')
print(f"dialog_title ==== {dialog_title}")
@st.dialog(dialog_title)
def show_contact_form(content):
    book_request_form(content)

@st.dialog(content.get('newRequestSummary', 'New Books'))
def new_book_summary():
    new_book_summary_form()

# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/profile.png", width=230)

with col2:
    st.title(content.get('searchVideo', 'Search Video'), anchor=False)
    st.write(
        content.get('svDescription', 'Search in 10,000 of audible books collection.')
    )
    if st.button(f"🛶 {content.get('bookRequest', 'New Book Request')}"):
        show_contact_form(content)

@st.cache_data
def load_zh_data():
    # Load and concatenate all CSV files
    csv_files = [
        'data/AudibleBook_new.csv',
        'data/SjClassics_new.csv',
    ]
    dataframes = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df


# Load data from CSV files
zh_data = load_zh_data()

@st.cache_data
def load_en_data():
    # Load and concatenate all CSV files
    csv_files = [
        'data/SpokenBooks_new.csv',
        'data/WClassics_new.csv'
    ]
    dataframes = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df


# Load data from CSV files
en_data = load_en_data()

if 'en' == language:
    data = en_data
else:
    data = zh_data

# Display the search input with a larger font and light blue color
st.markdown(
    f"""
    <style>
    .big-light-blue {{
        font-size: 24px; /* Adjust the font size as needed */
        color: #ADD8E6; /* Light blue color */
    }}
    </style>
    <div class="big-light-blue">{content.get('searchInput', 'Enter book name or author name to search, e.g. "Peace":')}</div>
    """,
    unsafe_allow_html=True
)

# Streamlit user input for search
search_query = st.text_input("", "").strip()

# Check if the search query is less than 3 characters
if len(search_query) > 0 and len(search_query) < 2:
    st.warning(content.get('svLengthWarning', "Please enter at least 2 characters to perform a search."))

# Filter data based on the search query
if len(search_query) >= 2:
    search_query = search_query.lower()
    filtered_data = data[data['title'].str.contains(search_query, case=False, na=False)]
else:
    filtered_data = pd.DataFrame(columns=['title', 'url', 'publishedAt'])

# Pagination settings
items_per_page = 10
items_per_column = 5
columns_count = 2

total_count = len(filtered_data)
total_pages = max((total_count - 1) // items_per_page + 1, 1)  # Ensure at least 1 page if there are results

if total_pages > 0:
    # Display styled label
    st.markdown(
        f"""
        <style>
        .big-light-blue {{
            font-size: 24px; /* Adjust the font size as needed */
            color: #ADD8E6; /* Light blue color */
        }}
        </style>
        <div class="big-light-blue">{content.get('searchResult', "Page of Total Pages")} {total_pages}</div>
        """,
        unsafe_allow_html=True
    )

    # Streamlit pagination input
    page = st.number_input("", min_value=1, max_value=total_pages, value=1, step=1)

    # Get the subset of data for the current page
    start_index = (page - 1) * items_per_page
    end_index = min(start_index + items_per_page, total_count)
    current_page_data = filtered_data.iloc[start_index:end_index]

    # Create columns for layout
    recent_cols = st.columns(columns_count)

    for i in range(columns_count):
        with recent_cols[i]:
            for j in range(items_per_column):
                recent_index = i * items_per_column + j
                if recent_index < len(current_page_data):
                    row = current_page_data.iloc[recent_index]
                    video_title = row['title']
                    video_url = row['url']
                    st.write(video_title)
                    # st.video(video_url, width=356)
                    st_player(video_url, height=200)
else:
    st.write(content.get('svNoResult', "No search result, Please try again."))
