import streamlit as st
from chatbot import Chatbot

#initialize values
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

if ("terms_accepted" not in st.session_state):
    st.session_state.terms_accepted = False

chatbot = st.session_state.chatbot

st.title("Casy")

if (not st.session_state.terms_accepted):
    st.session_state.terms_accepted = st.checkbox("I have read and accepted the terms and conditions.")
    
    with st.expander("View Terms and Conditions"):
        st.write("""
        **Terms and Conditions**
        
        1. Your data will be used in accordance with our policies.
        2. You agree not to misuse the service.
        3. Any violations may lead to account suspension.
        4. For more information, please refer to our policy guidelines.
        """)
    submitted = st.button("Accept")
    if (submitted and not st.session_state.terms_accepted):
        st.warning('Please accept the terms and conditions to proceed to the survey!', icon="⚠️")
else:
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