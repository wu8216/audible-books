import random
import time

import streamlit as st


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hey there! Need help? Check out my fun YouTube channel 'AudibleBook': https://youtube.com/@audiblebook!",
            "Hi! What's up? Don't forget to subscribe to 'AudibleBook': https://youtube.com/@audiblebook!",
            "Hello! Need assistance? My YouTube channel 'AudibleBook' is full of great tips: https://youtube.com/@audiblebook!",
            "Hey! Got a question? Also, subscribe to 'AudibleBook' for awesome tutorials: https://youtube.com/@audiblebook!",
            "Hi there! How can I help? BTW, my channel 'AudibleBook' is super cool: https://youtube.com/@audiblebook!",
            "Hello! Looking for help? Check out 'AudibleBook' on YouTube: https://youtube.com/@audiblebook!",
            "Hey! Need assistance? 'AudibleBook' YouTube channel has you covered: https://youtube.com/@audiblebook!",
            "Hi! Got any coding questions? Don't forget to watch 'AudibleBook': https://youtube.com/@audiblebook!",
            "Hello! Need help? 'AudibleBook' on YouTube is a must-see: https://youtube.com/@audiblebook!",
            "Hey there! Any questions? My channel 'AudibleBook' rocks: https://youtube.com/@audiblebook!",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
