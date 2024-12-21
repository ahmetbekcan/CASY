import streamlit as st
from helpers.utils import log_chat_input, get_current_survey_id
from database.database_wrapper import DatabaseWrapper

class ChatUI:
    def __init__(self):
        self.chatbot = st.session_state.chatbot
        self.initialize_messages()
        self.messages = st.session_state.messages

    def initialize_messages(self):
        if (not st.session_state.messages == []):
            return
        get_current_survey_id()
        db = DatabaseWrapper()
        
        survey_questions = db.fetch_all("""
                                        SELECT 
                                            questions.question_text, questions.id
                                        FROM surveys
                                        JOIN questions ON surveys.id = questions.survey_id
                                        WHERE surveys.id = ?;
                                    """, (st.session_state.cached_survey_id,))
        db.close()

        if survey_questions:
            for question in survey_questions:
                st.session_state.messages.append({"role": "assistant", "content": question["question_text"]})
                db2 = DatabaseWrapper()
                survey_answer = db2.fetch_one("""
                                                SELECT 
                                                    responses.response_text
                                                FROM responses
                                                JOIN questions ON questions.id = responses.question_id
                                                WHERE questions.id = ?;
                                            """, (question["id"],))
                db2.close()
                if (survey_answer):
                    st.session_state.messages.append({"role": "user", "content": survey_answer[0]})

    def append_and_log(self, dict):
        st.session_state.messages.append(dict)
        log_chat_input()

    def render(self):
        for message in self.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if self.messages == []:
            initial_message = st.write_stream(st.session_state.chatbot.ask_model([{"role": "user", "content": "Hi!"}]))
            self.append_and_log({"role": "assistant", "content": initial_message})
            st.rerun()

        # Accept user input
        if prompt := st.chat_input("Your answer"):
            self.append_and_log({"role": "user", "content": prompt})

            # Display the user message in the chat container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate the assistant's response
            with st.chat_message("assistant"):
                response = st.write_stream(self.chatbot.ask_model(self.messages))  # Get the response

            # Add the assistant's response to the chat history
            self.append_and_log({"role": "assistant", "content": response})