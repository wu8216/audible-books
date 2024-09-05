import streamlit as st

from forms.contact import contact_form


@st.dialog("Contact Team")
def show_contact_form():
    contact_form()


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/profile.png", width=230)

with col2:
    st.title("Audible Books", anchor=False)
    st.write(
        "A collection of audible books."
    )
    if st.button("✉️ Contact Us"):
        show_contact_form()


# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Channel Summary", anchor=False)
st.write(
    """
    The Audible Books Channel, launched in 2023, has quickly become a go-to destination for literary enthusiasts, offering an extensive collection of over 1,000 classic audiobooks. 
    Dedicated to preserving and sharing the timeless works of global literature, the channel covers a broad spectrum of historical periods, cultural backgrounds, and literary styles. 
    From beloved novels and thought-provoking essays to poetry and dramatic works, this channel provides a convenient and engaging way to experience the richness of world literature. 
    Committed to serving the community, the channel continues to expand its library, bringing more classic works to life through the power of audiobooks.
    """
)

# --- SKILLS ---
st.write("\n")
st.subheader("Team's Appreciation", anchor=False)
st.write(
    """
    Thank you for visiting our Audible Books Channel and taking the time to explore our collection of classic audiobooks. Your support and engagement mean the world to us, and we are thrilled to share these timeless literary works with you.
    We are dedicated to providing the best possible listening experience, and your feedback is invaluable in helping us achieve that goal. We warmly welcome any suggestions or comments you may have to improve the quality of our audiobooks and the channel as a whole. Whether it's about the narration, audio quality, or the selection of books, your insights will help us continue to serve you better.
    Please feel free to reach out to us with your thoughts. We look forward to hearing from you and thank you once again for being a part of our community.
    
    Best regards,
    The Audible Books Channel Team
    """
)
