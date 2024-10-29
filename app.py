import streamlit as st
from chatbot import Chatbot

# Initialize the chatbot only once
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

# Use the chatbot from session state
chatbot = st.session_state.chatbot

st.title("CASY")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant"):
        st.session_state.initial_message = st.write_stream(chatbot.ask_model([{"role": "user", "content": "Hi!"}]))

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.initial_message is not None:
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.initial_message })
    st.session_state.initial_message = None


# Accept user input
if prompt := st.chat_input("Your answer"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = st.write_stream(chatbot.ask_model(st.session_state.messages))  # Get the response
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})