import streamlit as st
import app as aps


# Apply CSS for styling
st.markdown("""
    <style>
    /* Global font settings */
    * {
        font-family: Google Sans, Helvetica Neue, sans-serif;
    }
    /* Title styling */
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: darkcyan;
        font-family: Google Sans, Helvetica Neue, sans-serif;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Custom title with the new class for styling
st.markdown("<h1 class='title'>Your Chatbot Assistant</h1>", unsafe_allow_html=True)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.spinner("Thinking..."):
        response = aps.llm_generator(prompt)
        print('Response: ',response)
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})