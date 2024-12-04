import streamlit as st
from database.database_wrapper import DatabaseWrapper
from typing import Tuple
from helpers.utils import render_logo

class LoginUI:
    def render(self):
        render_logo()
        st.title("Welcome to CASY!")
        tab1, tab2, tab3 = st.tabs(["Log In", "Sign Up", "Admin View"])
        with tab1:
            self.render_log_in()
        with tab2:
            self.render_sign_up()
        with tab3:
            self.render_admin_view()

    def render_sign_up(self):
        st.header("Sign Up")
        username = st.text_input("Username", key="signup_username")
        password = st.text_input("Password", type="password", key="signup_password")
        name = st.text_input("Name", key="signup_name")
        surname = st.text_input("Surname", key="signup_surname")
        company = st.text_input("Current/Most Recent Company", key="signup_company")

        if st.button("Sign Up"):
            success, message = self.sign_up_user(name, surname, company, username, password)
            if success:
                st.success(message)
            else:
                st.error(message)

    def render_log_in(self):
        st.header("Log In")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Log In"):
            success, message = self.log_in(username, password)
            if success:
                st.success(message)
                st.write(f"Welcome back, {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error(message)

    def render_admin_view(self):
        st.header("Admin View")
        admin_password = st.text_input("Enter Admin Password", type="password", key="admin_password")

        if st.button("View Registered Users"):
            if admin_password == "casy123":
                db = DatabaseWrapper()
                rows = db.fetch_all("SELECT id, name, surname, company, username FROM users")
                db.close()
                if rows:
                    st.subheader("Registered Users")
                    for row in rows:
                        st.write(f"ID: {row[0]}, Name: {row[1]}, Surname: {row[2]}, Company: {row[3]}, Username: {row[4]}")
                else:
                    st.write("No registered users found.")
            else:
                st.error("Incorrect admin password.")

        if st.button("View Created Survey Sessions"):
            if admin_password == "casy123":
                db = DatabaseWrapper()
                rows = db.fetch_all("SELECT session_name, session_code, creator_id, created_at FROM survey_sessions")

                if rows:
                    st.subheader("Created Survey Sessions")
                    for row in rows:
                        created_by = db.fetch_one("SELECT username FROM users WHERE id = ?",(row[2],))
                        st.write(f"Session Name: {row[0]}, Session Code: {row[1]}, Created By: {created_by[0]}, Creation Date: {row[3]}")
                else:
                    st.write("No created survey session found.")

                db.close()
            else:
                st.error("Incorrect admin password.")

    def sign_up_user(self, name: str, surname: str, company: str, username: str, password: str) -> Tuple[bool, str]:
        if not name or not surname:
            return False, "Name and Surname cannot be empty."
        if not company:
            return False, "Company name cannot be empty."
        if not username:
            return False, "Username cannot be empty."
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        try:
            db = DatabaseWrapper()
            db.execute_query("""
                INSERT INTO users (name, surname, company, username, password)
                VALUES (?, ?, ?, ?, ?)
            """, (name, surname, company, username, password))
            db.close()
            return True, "Account created successfully!"
        except:
            return False, "Username already exists. Please use a different username."

    def log_in(self, username: str, password: str) -> Tuple[bool, str]:
        if not username:
            return False, "Username cannot be empty."
        try:
            db = DatabaseWrapper()
            result = db.fetch_one("SELECT password FROM users WHERE username = ?", (username,))
            db.close()
            if result is None:
                return False, "Username does not exist. Please sign up first."
            if result[0] != password:
                return False, "Incorrect password. Please try again."
            return True, "Login successful!"
        except Exception as e:
            return False, f"An error occurred: {e}"