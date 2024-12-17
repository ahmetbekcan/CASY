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
                st.session_state.created_survey_session_code = survey_code
                st.success(f"survey '{self.created_survey_session_name}' created successfully!")
            except:
                st.error("A survey with this code already exists. Try again.")
        else:
            st.error("Please enter a survey name before creating a survey.")
    
    def display_survey_details(self,survey_id):
        db = DatabaseWrapper()
        
        survey_details = db.fetch_all("""
                                        SELECT 
                                            users.name AS participant_name,
                                            users.surname AS participant_surname,
                                            users.company AS participant_company,
                                            questions.question_text,
                                            responses.response_text
                                        FROM surveys
                                        JOIN survey_sessions ON surveys.session_id = survey_sessions.id
                                        JOIN users ON surveys.participant_id = users.id
                                        JOIN questions ON surveys.id = questions.survey_id
                                        JOIN responses ON questions.id = responses.question_id
                                        WHERE surveys.id = ?;
                                    """, (survey_id,))
        db.close()

        if survey_details:
            st.write(f"Participant: {survey_details[0]['participant_name']} {survey_details[0]['participant_surname']}")
            st.write(f"Company: {survey_details[0]['participant_company']}")
            
            st.write("### Survey Questions and Answers:")
            for detail in survey_details:
                st.write(f"**Question:** {detail['question_text']}")
                st.write(f"**Answer:** {detail['response_text']}")
        else:
            st.write("No details found for this survey.")

    def render_researcher_ui(self):
        st.title("Create a survey")

        if not st.session_state.created_survey_session_code:
            self.created_survey_session_name = st.text_input("Enter a survey name:", placeholder="e.g., MySurvey123")
            st.button("Create Survey survey", on_click=self.create_survey_session)

        # Show survey code and copy button if a survey is created
        if st.session_state.created_survey_session_code:
            st.write("### Your survey Code:")
            st.code(st.session_state.created_survey_session_code, language="text")
            st.download_button(
                "Save as text file!",
                data=st.session_state.created_survey_session_code,
                file_name="survey_code.txt",
                mime="text/plain",
            )

        completed_surveys = get_completed_surveys()
        if completed_surveys:
            st.title("Completed surveys")
            for survey in completed_surveys:
                with st.expander(f"Name: {survey['session_name']} - Session Code: {survey['session_code']}"):
                    st.write(f"Completed At: {survey['created_at']}")
                    if st.button(f"View Details for Survey ID {survey['survey_id']}"):
                        self.display_survey_details(survey['survey_id'])

    def join_survey(self):
        if (self.entered_survey_session_code):
            db = DatabaseWrapper()
            result = db.fetch_one("SELECT 1 FROM survey_sessions WHERE session_code = ?", (self.entered_survey_session_code,))
            db.close()
            if (result is not None):
                db = DatabaseWrapper()
                is_completed_before = db.fetch_one("""
                                                    SELECT 1
                                                    FROM surveys
                                                    JOIN survey_sessions ON surveys.session_id = survey_sessions.id
                                                    JOIN users ON surveys.participant_id = users.id
                                                    WHERE users.username = ? 
                                                    AND survey_sessions.session_code = ? 
                                                    AND surveys.is_completed = TRUE
                                                    LIMIT 1;
                                                """, (st.session_state.username, self.entered_survey_session_code))
                db.close()
                if (is_completed_before):
                    st.error("You have already completed this survey!")
                    return

                st.session_state.joined_survey_session_code = self.entered_survey_session_code
                st.session_state.user_role = UserRole.PARTICIPANT
            else:
                st.error("Survey session code is not valid.")
        else:
            st.error("Please enter a survey code to join a survey.")
            return False
        
    def render_participant_ui(self):
        st.title("Join a survey")
        self.entered_survey_session_code = st.text_input("Enter a survey code:")
        st.button("Join Survey", on_click=self.join_survey)

    def render(self):
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