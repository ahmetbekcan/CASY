import streamlit as st

class DeveloperSettingsUI:
    def __init__(self, chatbot):
        # Initialize the class with the chatbot instance to interact with session state
        self.chatbot = chatbot

    def render(self):
        with st.sidebar:
            with st.expander("Developer settings"):
                # Temperature slider
                temperature = st.slider(
                    "Temperature (controls randomness of the generations)",
                    min_value=0.0,
                    max_value=2.0,
                    value=self.chatbot.temperature,
                    step=0.1
                )

                # Maximum Tokens slider
                max_tokens = st.slider(
                    "Maximum Tokens",
                    min_value=1,
                    max_value=2048,
                    value=self.chatbot.max_tokens,
                    step=1
                )

                # Top P slider
                top_p = st.slider(
                    "Top P (fraction of most likely next words to sample)",
                    min_value=0.0,
                    max_value=0.99,
                    value=self.chatbot.top_p,
                    step=0.01
                )

                # Apply Settings button
                st.button(
                    "Apply Settings", 
                    on_click=self._apply_settings, 
                    args=(temperature, max_tokens, top_p)
                )

    def _apply_settings(self, temperature, max_tokens, top_p):
        # Apply the settings to the chatbot instance
        self.chatbot.set_parameters(temperature=temperature, max_tokens=max_tokens, top_p=top_p)
        st.success("Settings applied successfully!")
