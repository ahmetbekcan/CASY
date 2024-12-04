import streamlit as st
from helpers.utils import *
import random
import string
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    NONE = 1,
    RESEARCHER = 2,
    PARTICIPANT = 3

class UserRoleUI:
    def __init__(self):
        self.created_survey_session_name = None
        self.entered_survey_session_code = None

    def save_session_to_db(self, session_code):
        db = DatabaseWrapper()
        print(st.session_state.username)
        id = db.fetch_one("SELECT id FROM users WHERE username = ?", (st.session_state.username,))
        db.execute_query("""
                INSERT INTO survey_sessions (session_name, session_code, creator_id)
                VALUES (?, ?, ?)
            """, (self.created_survey_session_name, session_code, id[0]))
        db.close()

    def create_survey_session(self):
        if self.created_survey_session_name:
            # Generate a unique survey code (e.g., 8 characters long)
            survey_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            try:
                self.save_session_to_db(survey_code)
                st.session_state["created_survey_session_code"] = survey_code
                st.success(f"survey '{self.created_survey_session_name}' created successfully!")
            except:
                st.error("A survey with this code already exists. Try again.")
        else:
            st.error("Please enter a survey name before creating a survey.")

    def render_researcher_ui(self):
        st.title("Create a survey")

        if not st.session_state["created_survey_session_code"]:
            self.created_survey_session_name = st.text_input("Enter a survey name:", placeholder="e.g., MySurvey123")
            st.button("Create Survey survey", on_click=self.create_survey_session)

        # Show survey code and copy button if a survey is created
        if st.session_state["created_survey_session_code"]:
            st.write("### Your survey Code:")
            st.code(st.session_state["created_survey_session_code"], language="text")
            st.download_button(
                "Save as text file!",
                data=st.session_state["created_survey_session_code"],
                file_name="survey_code.txt",
                mime="text/plain",
            )

    def join_survey(self):
        if (self.entered_survey_session_code):
            db = DatabaseWrapper()
            result = db.fetch_one("SELECT 1 FROM survey_sessions WHERE session_code = ?", (self.entered_survey_session_code,))
            if (result is not None):
                st.session_state["joined_survey_session_code"] = self.entered_survey_session_code
                st.session_state["user_role"] = UserRole.PARTICIPANT
            else:
                st.error("Survey session code is not valid.")
        else:
            st.error("Please enter a survey code to join a survey.")
            return False
        
    def render_participant_ui(self):
        st.title("Join a survey")
        self.entered_survey_session_code = st.text_input("Enter a survey code:")
        st.button("Join Survey survey", on_click=self.join_survey)
        if (st.session_state["user_role"] == UserRole.PARTICIPANT):
            st.rerun()

    def render(self):
        if "user_role" not in st.session_state:
            st.session_state["user_role"] = UserRole.NONE
            
        if "created_survey_session_code" not in st.session_state:
            st.session_state["created_survey_session_code"] = None

        if "joined_survey_session_code" not in st.session_state:
            st.session_state["joined_survey_session_code"] = None

        render_logo()
        st.title("Who are you?",)
        tab1, tab2, tab3 = st.tabs(["I am a researcher", "I am a participant", "Other"])
        with tab1:
            self.render_researcher_ui()
        with tab2:
            self.render_participant_ui()
        with tab3:
            if (st.button("Log Out")):
                st.session_state.clear()
                st.rerun()