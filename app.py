import streamlit as st
from models.chatbot import Chatbot
from models.agent import Agent
from test.survey_simulator import SurveySimulator

def read_file_to_variable(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

#initialize values
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

if "participant" not in st.session_state:
    st.session_state.participant = Agent()
    instruct = "Your goal is to answer survey questions. You should only answer the questions by using your background.\
                You shouldn't ask any questions.\n" + read_file_to_variable("test_data/alex.txt") 
    st.session_state.participant.set_instruct(instruct)

if ("terms_accepted" not in st.session_state):
    st.session_state.terms_accepted = False

if ("evaluation" not in st.session_state):
    st.session_state.evaluation = ""

if ("survey_completed" not in st.session_state):
    st.session_state.survey_completed = False
#initialize values

#initialize agents
chatbot = st.session_state.chatbot
participant = st.session_state.participant
#initialize agents

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
            st.session_state.initial_message = st.write_stream(chatbot.ask_model([{"role": "user", "content": "Hi!"}]))

def simulate_survey():
    simulator = SurveySimulator(number_of_questions=no_of_questions,
                                offtopic_answer_rate=rate_of_offtopic,
                                uninformative_answer_rate=rate_of_uninformative,
                                initial_messages=st.session_state.messages)
    simulator.simulate(chatbot,participant)
    st.session_state.messages = simulator.get_simulation_result()
    

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
    res = ''.join(chatbot.ask_model(st.session_state.messages))
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
        with st.expander("Survey Simulation"):
            no_of_questions = st.slider("Number Of Questions", min_value=1,max_value=30,value=5,step=1)
            rate_of_offtopic = st.slider("Offtopic Answer Rate", min_value=0.,max_value=1.,value=0.1,step=0.01)
            rate_of_uninformative = st.slider("Uninformative Answer Rate", min_value=0.,max_value=1.,value=0.1,step=0.01)
            st.button('Simulate Survey', on_click=simulate_survey)
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
                value=chatbot.temperature,
                step=0.1
            )

            max_tokens = st.slider(
                "Maximum Tokens",
                min_value=1,
                max_value=2048,
                value=chatbot.max_tokens,
                step=1
            )

            top_p = st.slider(
                "Top P (fraction of most likely next words to sample)",
                min_value=0.0,
                max_value=0.99,
                value=chatbot.top_p,
                step=0.01
            )
            st.button("Apply Settings", on_click=chatbot.set_parameters(temperature=temperature,max_tokens=max_tokens,top_p=top_p))
        
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
            response = st.write_stream(chatbot.ask_model(st.session_state.messages))  # Get the response
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
#UI