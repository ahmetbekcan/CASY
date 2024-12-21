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

                    1. Data Controller
                    This information text is prepared in accordance with the Personal Data Protection Law No. 6698
                    ("KVKK"). Your personal data is processed by CASY/METU within the scope described below.
                    2. Purpose of Processing Personal Data
                    Your personal data, including but not limited to name, email address, and survey responses, is
                    collected and processed for the following purposes:
                    • Conducting chatbot-based surveys,
                    • Gathering insights on technical challenges,
                    • Improving and analyzing chatbot performance,
                    • Ensuring secure and effective use of the chatbot service.
                    3. Legal Basis and Method of Data Collection
                    Personal data is collected electronically via the chatbot platform based on the legal grounds of
                    explicit consent (Article 5/1 of KVKK) and/or the legitimate interest of the data controller
                    (Article 5/2-f).
                    4. Data Sharing
                    Your personal data will not be shared with third parties without your explicit consent, except
                    where legally required or within the scope of collaborations for academic and research purposes.
                    5. Storage and Security
                    Your data will be securely stored in Google Cloud for the duration necessary to achieve the
                    stated purposes. Appropriate technical and organizational measures are taken to protect your
                    personal data against unauthorized access.
                    6. Rights of Data Subjects
                    Under KVKK, you have the right to:
                    • Learn whether your data is being processed,
                    • Request information regarding the processing,
                    • Access your data and request corrections,
                    • Request the deletion/destruction of your data,
                    • Object to the processing or request limitation,
                    • Lodge a complaint with the Personal Data Protection Authority.
                    """)

                terms_accepted = st.checkbox("I have read and accepted the terms and conditions.")
                submitted = st.form_submit_button(label="Proceed To Survey",use_container_width=True,)
                
                if submitted:
                    if terms_accepted:
                        st.session_state.terms_accepted = True
                        log_survey()
                        st.rerun()
                    else:
                        st.warning('Please accept the terms and conditions to proceed to the survey!', icon="⚠️")
            
            if (st.button("Cancel Survey")):
                st.session_state.joined_survey_session_code = None
                st.session_state.user_role = UserRole.NONE
                st.rerun()