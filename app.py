import streamlit as st
from chatbot import Chatbot
from agent import Agent
import copy

def read_file_to_variable(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

#initialize values
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

if "participant" not in st.session_state:
    st.session_state.participant = Agent()
    #instruct = read_file_to_variable("test_data/participant_instruct.txt") + read_file_to_variable("test_data/alex.txt") 
    instruct = "Your goal is to answwer survey questions. You should only answer the questions by using your background. You shouldn't ask any questions.\n" + read_file_to_variable("test_data/alex.txt") 
    st.session_state.participant.set_instruct(instruct)

if ("terms_accepted" not in st.session_state):
    st.session_state.terms_accepted = False

chatbot = st.session_state.chatbot
participant = st.session_state.participant

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

def clear_chat_history():
        st.session_state.messages = []
        with st.chat_message("assistant"):
            st.session_state.initial_message = st.write_stream(chatbot.ask_model([{"role": "user", "content": "Hi!"}]))

def reverse_message_roles(msgs):
    for msg in msgs:
        if (msg['role'] == "user"):
            msg['role'] = "assistant"
        else:
            msg['role'] = "user"

def simulate_answer():
    reverse_message_roles(st.session_state.messages)
    res = ''.join(participant.ask_model(st.session_state.messages))
    reverse_message_roles(st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": res})
    if res:
        res2 = ''.join(chatbot.ask_model(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": res2})
        if res2:
            reverse_message_roles(st.session_state.messages)
            res3 = ''.join(participant.ask_model(st.session_state.messages))
            reverse_message_roles(st.session_state.messages)
            st.session_state.messages.append({"role": "user", "content": res3})

def simulate_answers():
    i = 0
    while (i < no_of_questions):
        simulate_answer()
        i+=1

if (st.session_state.terms_accepted):
    # Initialize chat history
    if "messages" not in st.session_state:
        clear_chat_history()

    with st.sidebar:
        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
        with st.expander("Survey Simulation"):
            no_of_questions = st.slider("Number of questions", min_value=1,max_value=10,value=3,step=1)
            st.button('Simulate Survey', on_click=simulate_answers)

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

            # Slider for max tokens
            max_tokens = st.slider(
                "Maximum Tokens",
                min_value=1,
                max_value=2048,
                value=chatbot.max_tokens,
                step=1
            )

            # Slider for top_p
            top_p = st.slider(
                "Top P (fraction of most likely next words to sample)",
                min_value=0.0,
                max_value=0.99,
                value=chatbot.top_p,
                step=0.01
            )
            st.button("Apply Settings", on_click=chatbot.set_parameters(temperature=temperature,max_tokens=max_tokens,top_p=top_p))
        
    # Display chat messages from history on app rerun
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