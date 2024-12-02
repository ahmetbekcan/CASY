import streamlit as st
import ui_components
from utils import *
from ui_components.user_role_ui import UserRole

class MainUI:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def clear_chat_history(self):
        st.session_state.messages = []
        with st.chat_message("assistant"):
            st.session_state.initial_message = st.write_stream(st.session_state.chatbot.ask_model([{"role": "user", "content": "Hi!"}]))

    def complete_survey(self):
        st.session_state.messages.append({"role": "user", "content": "End the survey. Don't ask any further questions."})
        res = ''.join(st.session_state.chatbot.ask_model(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": res})
        st.session_state.survey_completed = True
    
    def log_out(self):
        st.session_state.clear()

    def render_terms_and_conditions(self):
        ui_terms_conditions = ui_components.TermsAndConditionsUI()
        ui_terms_conditions.render()

    def render_survey_simulation(self):
        ui_survey_simulation = ui_components.SurveySimulationUI(self.chatbot)
        ui_survey_simulation.render()

    def render_survey_evaluator(self):
        ui_survey_evaluator = ui_components.SurveyEvaluatorUI()
        ui_survey_evaluator.render()

    def render_developer_settings(self):
        ui_dev_settings = ui_components.DeveloperSettingsUI(self.chatbot)
        ui_dev_settings.render()

    def render_chat_ui(self):
        ui_chat = ui_components.ChatUI(self.chatbot)
        ui_chat.render()

    def render_login_ui(self):
        ui_login = ui_components.LoginUI()
        ui_login.render()

    def render_user_role_ui(self):
        user_role_ui = ui_components.UserRoleUI()
        user_role_ui.render()

    def render_survey_ui(self):
        if "messages" not in st.session_state:
            self.clear_chat_history()
        
        # Left side
        with st.sidebar:
            st.button("Complete Survey", on_click=self.complete_survey)
            st.button('Clear Survey', on_click=self.clear_chat_history)
            st.button("Log out", on_click=self.log_out)
            if (st.session_state.user_id == "casy"):
                self.render_survey_simulation()
                self.render_survey_evaluator()
                self.render_developer_settings()

        # Chat in the right side
        self.render_chat_ui()
    
    def render(self):

        if not st.session_state.get("css", None):
            st.session_state.css = read_file("ui_components/styles.css")
        st.markdown(f"<style>{st.session_state.css}</style>", unsafe_allow_html=True) #Global app style can be set here

        if not st.session_state.get("logged_in", False):
            self.render_login_ui()
            return

        if (st.session_state.get("user_role", UserRole.NONE) == UserRole.NONE):
            self.render_user_role_ui()
            return

        if (not st.session_state.user_id == "casy"):
            if not st.session_state.get("terms_accepted", False):
                self.render_terms_and_conditions()
                return

        self.render_survey_ui()
        
