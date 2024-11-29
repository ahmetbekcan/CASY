import streamlit as st
from models.agent import Agent

class SurveyEvaluator:
    def __init__(self, chatbot):
        self.chatbot = chatbot
        self.evaluation_result = st.session_state.get("evaluation", None)

    def evaluate(self):
        # Initialize evaluator agent
        evaluator = Agent()
        evaluator.instruct = (
            "You are an evaluator. You will evaluate the given survey questions that are asked by the assistant. "
            "You should only evaluate the behaviour of the assistant. "
            "Behaviour of the user should not affect the evaluation quality. "
            "You should only evaluate the questions based on their relevancy to technical debt, "
            "follow-up rate (the rate of follow-up questions that are asked when necessary), "
            "and uniqueness (the percentage of questions that are different). "
            "You should represent the results by listing them in percentages such as:\n"
            "Relevancy: 80%\n"
            "Follow-up rate: 50%\n"
            "Uniqueness: 90%\n"
            "You should not write any other thing than that."
        )

        # Ask the model and get the evaluation result
        evaluation_response = ''.join(evaluator.ask_model(st.session_state.messages))
        self.evaluation_result = evaluation_response
        st.session_state.evaluation = self.evaluation_result

    def render(self):
        # Survey evaluation UI
        with st.expander("Survey Evaluation"):
            st.button("Evaluate", on_click=self.evaluate)  # Trigger the evaluation
            if self.evaluation_result:
                st.write(self.evaluation_result)  # Display the evaluation result
