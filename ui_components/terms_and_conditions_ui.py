import streamlit as st
from ui_components.user_role_ui import UserRole
from helpers.utils import *

class TermsAndConditionsUI:
    def __init__(self):
        # Store the acceptance state in session state for persistence
        self.terms_accepted = st.session_state.terms_accepted

    def render(self):
        # If the user has accepted the terms, don't show the form
        if not self.terms_accepted:
            render_logo()

            # Create form to accept terms
            with st.form("terms"):
                with st.expander("⚖️ View Terms and Conditions"):
                    st.write("""
                    **Terms and Conditions**

                    1. Your data will be used in accordance with our policies.
                    2. You agree not to misuse the service.
                    3. Any violations may lead to account suspension.
                    4. For more information, please refer to our policy guidelines.
                    """)

                terms_accepted = st.checkbox("I have read and accepted the terms and conditions.")
                submitted = st.form_submit_button(label="Proceed To Survey",use_container_width=True,)
                
                if submitted:
                    if terms_accepted:
                        st.session_state.terms_accepted = True
                        st.rerun()
                    else:
                        st.warning('Please accept the terms and conditions to proceed to the survey!', icon="⚠️")
            
            if (st.button("Cancel Survey")):
                st.session_state.joined_survey_session_code = None
                st.session_state.user_role = UserRole.NONE
                st.rerun()