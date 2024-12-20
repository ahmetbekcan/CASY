import streamlit as st
from tests.survey_test import *

class SurveySimulationUI:
    def __init__(self):
        self.no_of_questions = 5
        self.rate_of_normal = 0.8
        self.rate_of_offtopic = 0.1
        self.rate_of_uninformative = 0.1
        self.chatbot = st.session_state.chatbot
        self.agent = "Alex"
        self.log_data = False
    def render(self):
        with st.expander("Survey Simulation"):
            self.agent = st.radio(
                            "Select a character:",
                            ("Alex", "Ada", "Andrew"),index=0
                        )
            
            self.no_of_questions = st.slider(
                "Number Of Questions", min_value=1, max_value=30, value=self.no_of_questions, step=1
            )
            self.rate_of_normal = st.slider(
                "Normal Answer Weight", min_value=0.0, max_value=1.0, value=self.rate_of_normal, step=0.01
            )
            self.rate_of_offtopic = st.slider(
                "Offtopic Answer Weight", min_value=0.0, max_value=1.0, value=self.rate_of_offtopic, step=0.01
            )
            self.rate_of_uninformative = st.slider(
                "Uninformative Answer Weight", min_value=0.0, max_value=1.0, value=self.rate_of_uninformative, step=0.01
            )
            st.button(
                'Simulate Survey',
                on_click=self.simulate_survey,
            )
            self.log_data = st.checkbox("Log Data",self.log_data)

    def simulate_survey(self):
        simulator = SurveySimulator(
            number_of_questions=self.no_of_questions,
            normal_answer_weight = self.rate_of_normal,
            offtopic_answer_weight=self.rate_of_offtopic,
            uninformative_answer_weight=self.rate_of_uninformative,
            initial_messages=st.session_state.messages,
            agent = self.agent,
            log_data=self.log_data
        )
        simulator.set_surveyor(self.chatbot)
        simulator.simulate()
        st.session_state.messages = simulator.get_simulation_messages()