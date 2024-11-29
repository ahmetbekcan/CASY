import streamlit as st
from models.chatbot import Chatbot
from models.agent import Agent
from UIElements.SurveySimulationUI import SurveySimulationUI

#initialize values
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

if ("terms_accepted" not in st.session_state):
    st.session_state.terms_accepted = False

if ("evaluation" not in st.session_state):
    st.session_state.evaluation = ""

if ("survey_completed" not in st.session_state):
    st.session_state.survey_completed = False
#initialize values

#Terms and conditions
with st.sidebar:
    st.title("🤖 Casy")
    st.caption("Survey chatbot")
    if(not st.session_state.terms_accepted):
        with (st.form("terms")):
            terms_accepted = st.checkbox("I have read and accepted the terms and conditions.")
            with st.expander("⚖️ View Terms and Conditions"):
                st.write("""
                **Terms and Conditions**
                
                1. Your data will be used in accordance with our policies.
                2. You agree not to misuse the service.
                3. Any violations may lead to account suspension.
                4. For more information, please refer to our policy guidelines.
                """)
            submitted = st.form_submit_button()
            if (submitted and not terms_accepted):
                st.warning('Please accept the terms and conditions to proceed to the survey!', icon="⚠️")
        if (submitted):
            st.session_state.terms_accepted = terms_accepted
#Terms and conditions

#Events
def clear_chat_history():
    st.session_state.messages = []
    with st.chat_message("assistant"):
        st.session_state.initial_message = st.write_stream(st.session_state.chatbot.ask_model([{"role": "user", "content": "Hi!"}]))    

def evaluate_survey():
    evaluator = Agent()
    evaluator.instruct="You are an evaluator. You will evaluate the given survey questions that are asked by the assistant. \
                        You should only evaluate the behaviour of the assistant.\
                        Behaivour of the user should not affect the evaluation quality.\
                        You should only evaluate the questions based on their relevancy to technical debt,\
                        follow up rate (the rate of follow up questions that are asked when necessary) \
                        and uniqueness (the percantage of questions that are different).\
                        You should represent the results by listing them in percentages such as \n\
                        Relevancy: 80%\n\
                        Follow-up rate: 50%\n\
                        Uniqueness: 90%\n\
                        You should not write any other thing than that."
    res = ''.join(evaluator.ask_model(st.session_state.messages))
    st.session_state.evaluation = res

def complete_survey():
    st.session_state.messages.append({"role": "user", "content": "End the survey. Don't ask any further questions."})
    res = ''.join(st.session_state.chatbot.ask_model(st.session_state.messages))
    st.session_state.messages.append({"role": "assistant", "content": res})
    st.session_state.survey_completed = True
#Events

#UI
if (st.session_state.terms_accepted):
    # Initialize chat history
    if "messages" not in st.session_state:
        clear_chat_history()

    with st.sidebar:
        st.button("Complete Survey", on_click=complete_survey)
        st.button('Clear Chat History', on_click=clear_chat_history)

        ui_survey_simulation = SurveySimulationUI(st.session_state.chatbot)
        ui_survey_simulation.render()

        with st.expander("Survey Evaluation"):
            st.button("Evaluate", on_click=evaluate_survey)
            if (st.session_state.evaluation is not None and st.session_state.evaluation != ""):
                st.write(st.session_state.evaluation)

    #Developer settings
    with st.sidebar:
        with st.expander("Developer settings"):
            temperature = st.slider(
                "Temperature (controls randomness of the generations)",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.chatbot.temperature,
                step=0.1
            )

            max_tokens = st.slider(
                "Maximum Tokens",
                min_value=1,
                max_value=2048,
                value=st.session_state.chatbot.max_tokens,
                step=1
            )

            top_p = st.slider(
                "Top P (fraction of most likely next words to sample)",
                min_value=0.0,
                max_value=0.99,
                value=st.session_state.chatbot.top_p,
                step=0.01
            )
            st.button("Apply Settings", on_click=st.session_state.chatbot.set_parameters(temperature=temperature,max_tokens=max_tokens,top_p=top_p))
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.initial_message is not None:
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.initial_message })
        st.session_state.initial_message = None


    # Accept user input
    if prompt := st.chat_input("Your answer"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = st.write_stream(st.session_state.chatbot.ask_model(st.session_state.messages))  # Get the response
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
#UI