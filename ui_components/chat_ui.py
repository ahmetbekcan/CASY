import streamlit as st

class ChatUI:
    def __init__(self, chatbot):
        self.chatbot = chatbot
        self.messages = st.session_state.get("messages", [])
        self.initial_message = st.session_state.get("initial_message", None)

    def render(self):
        for message in self.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if self.initial_message is not None:
            st.session_state.messages.append({"role": "assistant", "content": self.initial_message})
            st.session_state.initial_message = None

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