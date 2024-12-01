import streamlit as st
from tests.survey_test import SurveyEvaluator

class SurveyEvaluatorUI:
    def __init__(self):
        self.evaluation_result = st.session_state.get("evaluation", None)

    def evaluate(self):
        evaluator = SurveyEvaluator()
        evaluator._get_relevancy_evaluator()

    def render(self):
        # Survey evaluation UI
        with st.expander("Survey Evaluation"):
            st.button("Evaluate", on_click=self.evaluate)  # Trigger the evaluation
            if self.evaluation_result:
                st.write(self.evaluation_result)  # Display the evaluation result
