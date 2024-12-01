import streamlit as st
from typing import Tuple

# Initialize session state for user database
if "user_db" not in st.session_state:
    st.session_state["user_db"] = {}
class LoginUI:
    def render(self):
        st.title("Welcome to CASY! Login or Sign-Up")
        # Create tabs for "Log In" and "Sign Up"
        tab1, tab2 = st.tabs(["Log In", "Sign Up"])
        with tab1:
            self.render_log_in()
        with tab2:
            self.render_sign_up()

    def render_sign_up(self):
        st.header("Sign Up")
        username = st.text_input("Enter Username/Email", key="signup_username")
        password = st.text_input("Enter Password", type="password", key="signup_password")

        if st.button("Sign Up"):
            success, message = self.sign_up_user(username, password)
            if success:
                st.success(message)
            else:
                st.error(message)

    def render_log_in(self):
        st.header("Log In")
        username = st.text_input("Enter Username/Email", key="login_username")
        password = st.text_input("Enter Password", type="password", key="login_password")

        if st.button("Log In"):
            success, message = self.log_in(username, password)
            if success:
                st.success(message)
                st.write(f"Welcome back, {username}!")
            else:
                st.error(message)

    def sign_up_user(self, username: str, password: str) -> Tuple[bool, str]:
        """ Signs up a new user by validating the username and password.
        Parameters:
        - username (str): The username or email for the account.
        - password (str): The password for the account.
        Returns:
        - Tuple[bool, str]: (True, success message) if successful,
                            (False, error message) if validation fails.
        """
        user_db = st.session_state["user_db"]  # Access session state user database

        if not username:
            return False, "Username cannot be empty."
        
        if username in user_db:
            return False, "Username already exists. Please choose a different username."
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        user_db[username] = password
        return True, "Account created successfully!"

    def log_in(self, username: str, password: str) -> Tuple[bool, str]:
        """ Logs in an existing user by validating their credentials.
        Parameters:
        - username (str): The username or email of the account.
        - password (str): The password for the account.
        Returns:
        - Tuple[bool, str]: (True, success message) if successful,
                            (False, error message) if validation fails."""
        user_db = st.session_state["user_db"]  # Access session state user database

        if not username:
            return False, "Username cannot be empty."
        
        if username not in user_db:
            return False, "Username does not exist. Please sign up first."
        
        if user_db[username] != password:
            return False, "Incorrect password. Please try again."
        
        return True, "Login successful!"

if __name__ == "__main__":
    login_ui = LoginUI()
    login_ui.render()
