import streamlit as st
from utils import *
import sqlite3
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
        self.created_survey_name = None
        self.entered_survey_code = None

    def save_survey_to_db(self, survey_code):
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect("app_data.db") as conn:
            conn.execute("""
                INSERT INTO surveys (survey_name, survey_code, creator_username, creation_date)
                VALUES (?, ?, ?, ?)
            """, (self.created_survey_name, survey_code, st.session_state.user_id, creation_date))
            conn.commit()

    def create_survey(self):
        if self.created_survey_name:
            # Generate a unique survey code (e.g., 8 characters long)
            survey_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            try:
                self.save_survey_to_db(survey_code)
                st.session_state["created_survey_code"] = survey_code
                st.success(f"survey '{self.created_survey_name}' created successfully!")
            except sqlite3.IntegrityError:
                st.error("A survey with this code already exists. Try again.")
        else:
            st.error("Please enter a survey name before creating a survey.")

    def render_researcher_ui(self):
        st.title("Create a survey")

        if not st.session_state["created_survey_code"]:
            self.created_survey_name = st.text_input("Enter a survey name:", placeholder="e.g., MySurvey123")
            st.button("Create Survey survey", on_click=self.create_survey)

        # Show survey code and copy button if a survey is created
        if st.session_state["created_survey_code"]:
            st.write("### Your survey Code:")
            st.code(st.session_state["created_survey_code"], language="text")
            st.download_button(
                "Save as text file!",
                data=st.session_state["created_survey_code"],
                file_name="survey_code.txt",
                mime="text/plain",
            )

    def join_survey(self):
        if (self.entered_survey_code):
            with sqlite3.connect("app_data.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM surveys WHERE survey_code = ?", (self.entered_survey_code,))
                result = cursor.fetchone()
                st.session_state["joined_survey_code"] = self.entered_survey_code
                st.session_state["user_role"] = UserRole.PARTICIPANT
                return result is not None
        else:
            st.error("Please enter a survey code to join a survey.")
            return False
        
    def render_participant_ui(self):
        st.title("Join a survey")
        self.entered_survey_code = st.text_input("Enter a survey code:")
        st.button("Join Survey survey", on_click=self.join_survey)

    def render(self):
        if "created_survey_code" not in st.session_state:
            st.session_state["created_survey_code"] = None

        if "joined_survey_code" not in st.session_state:
            st.session_state["joined_survey_code"] = None

        render_logo()
        st.title("Who are you?",)
        tab1, tab2 = st.tabs(["I am a researcher", "I am a participant"])
        with tab1:
            self.render_researcher_ui()
        with tab2:
            self.render_participant_ui()