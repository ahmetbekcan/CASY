import streamlit as st
import ui_components
from models.large_language_models import Chatbot
from helpers.utils import initialize_database
from ui_components.user_role_ui import UserRole
from version import __version__

st.set_page_config(
    menu_items={
        'about': f'**CASY {__version__}**'
    }
)
# INITIALIZE SESSION STATE VARIABLES HERE

if ("chatbot" not in st.session_state):
    st.session_state.chatbot = Chatbot()

if ("terms_accepted" not in st.session_state):
    st.session_state.terms_accepted = False

if ("survey_completed" not in st.session_state):
    st.session_state.survey_completed = False

if ("css" not in st.session_state):
    st.session_state.css = None

if ("logged_in" not in st.session_state):
    st.session_state.logged_in = False

if ("username" not in st.session_state):
    st.session_state.username = ""

if ("user_role" not in st.session_state):
    st.session_state.user_role = UserRole.NONE

if ("created_survey_session_code" not in st.session_state):
    st.session_state.created_survey_session_code = None

if ("joined_survey_session_code" not in st.session_state):
    st.session_state.joined_survey_session_code = None

if ("messages" not in st.session_state):
    st.session_state.messages = []

if ("initial_message" not in st.session_state):
    st.session_state.initial_message = None

# CACHED DATABASE QUERIES
if ("cached_survey_id" not in st.session_state):
    st.session_state.cached_survey_id = None

if ("cached_user_id" not in st.session_state):
    st.session_state.cached_user_id = None

if ("cached_survey_session_id" not in st.session_state):
    st.session_state.cached_survey_session_id = None

initialize_database()

app_ui = ui_components.MainUI()
app_ui.render()