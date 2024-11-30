import streamlit as st
import ui_components
from models.large_language_models import *

if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

if ("terms_accepted" not in st.session_state):
    st.session_state.terms_accepted = False

if ("evaluation" not in st.session_state):
    st.session_state.evaluation = ""

if ("survey_completed" not in st.session_state):
    st.session_state.survey_completed = False

app_ui = ui_components.MainUI(st.session_state.chatbot)
app_ui.render()