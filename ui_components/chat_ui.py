import streamlit as st

class ChatUI:
    def __init__(self):
        self.chatbot = st.session_state.chatbot
        self.messages = st.session_state.messages

    def render(self):
        for message in self.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if self.messages == []:
            initial_message = st.write_stream(st.session_state.chatbot.ask_model([{"role": "user", "content": "Hi!"}]))
            st.session_state.messages.append({"role": "assistant", "content": initial_message})
            st.rerun()

        # Accept user input
        if prompt := st.chat_input("Your answer"):
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display the user message in the chat container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate the assistant's response
            with st.chat_message("assistant"):
                response = st.write_stream(self.chatbot.ask_model(self.messages))  # Get the response

            # Add the assistant's response to the chat history
            st.session_state.messages.append({"role": "assistant", "content": response})