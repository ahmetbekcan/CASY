import streamlit as st
import ui_components
from helpers.utils import *
from ui_components.user_role_ui import UserRole

class MainUI:
    def __init__(self):
        self.chatbot = st.session_state.chatbot

    def clear_chat_history(self):
        st.session_state.messages = []
        get_current_survey_id()
        db = DatabaseWrapper()
        db.execute_query("""
                            DELETE FROM responses WHERE question_id IN (
                                SELECT id FROM questions WHERE survey_id = ?
                            );
                        """, (st.session_state.cached_survey_id,))
        
        db.execute_query("DELETE FROM questions WHERE survey_id = ?;", (st.session_state.cached_survey_id,))
        db.close()

    def complete_survey(self):
        st.session_state.survey_completed = True
        get_current_survey_id()
        db = DatabaseWrapper()
        db.execute_query("""
                            UPDATE surveys
                            SET is_completed = TRUE
                            WHERE id = ?;
                        """, (st.session_state.cached_survey_id,))
        db.close()
        clear_cached_values()
        st.session_state.joined_survey_session_code = None
        
    def log_out(self):
        st.session_state.clear()
    
    def go_to_main_page(self):
        temp_username = st.session_state.username
        st.session_state.clear()
        st.session_state.username = temp_username
        st.session_state.logged_in = True

    def render_terms_and_conditions(self):
        ui_terms_conditions = ui_components.TermsAndConditionsUI()
        ui_terms_conditions.render()

    def render_survey_simulation(self):
        ui_survey_simulation = ui_components.SurveySimulationUI()
        ui_survey_simulation.render()

    def render_survey_evaluator(self):
        ui_survey_evaluator = ui_components.SurveyEvaluatorUI()
        ui_survey_evaluator.render()

    def render_developer_settings(self):
        ui_dev_settings = ui_components.DeveloperSettingsUI()
        ui_dev_settings.render()

    def render_chat_ui(self):
        ui_chat = ui_components.ChatUI()
        ui_chat.render()

    def render_login_ui(self):
        ui_login = ui_components.LoginUI()
        ui_login.render()

    def render_user_role_ui(self):
        user_role_ui = ui_components.UserRoleUI()
        user_role_ui.render()

    def render_survey_ui(self):
        # Left side
        with st.sidebar:
            st.button("Complete Survey", on_click=self.complete_survey)
            st.button('Clear Survey', on_click=self.clear_chat_history)
            st.button("Log out", on_click=self.log_out)
            if (st.session_state.username == "casy"):
                self.render_survey_simulation()
                self.render_survey_evaluator()
                self.render_developer_settings()

        # Chat in the right side
        self.render_chat_ui()
            
    def render_completion_ui(self):
        render_logo()
        st.title("Thanks for your participation!")
        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
            st.button("Main Page", on_click=self.go_to_main_page)
            st.button("Log out", on_click=self.log_out)

    def render(self):

        if (st.session_state.css == None):
            st.session_state.css = read_file("ui_components/styles.css")
        st.markdown(f"<style>{st.session_state.css}</style>", unsafe_allow_html=True) #Global app style can be set here

        if not st.session_state.logged_in:
            self.render_login_ui()
            return
        
        if (st.session_state.user_role == UserRole.NONE):
            self.render_user_role_ui()
            return
        
        if not st.session_state.terms_accepted:
            self.render_terms_and_conditions()
            return
        
        if (st.session_state.survey_completed):
            self.render_completion_ui()
            return
        
        self.render_survey_ui()
        
