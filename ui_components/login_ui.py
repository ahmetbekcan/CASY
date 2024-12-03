import streamlit as st
import sqlite3
from typing import Tuple
from utils import render_logo

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
                st.session_state.user_id = username
                st.rerun()
            else:
                st.error(message)

    def render_admin_view(self):
        st.header("Admin View")
        admin_password = st.text_input("Enter Admin Password", type="password", key="admin_password")

        if st.button("View Registered Users"):
            if admin_password == "casy123":
                conn = sqlite3.connect("app_data.db")
                c = conn.cursor()
                c.execute("SELECT name, surname, company, username FROM users")
                rows = c.fetchall()
                conn.close()

                if rows:
                    st.subheader("Registered Users")
                    for row in rows:
                        st.write(f"Name: {row[0]}, Surname: {row[1]}, Company: {row[2]}, Username: {row[3]}")
                else:
                    st.write("No registered users found.")
            else:
                st.error("Incorrect admin password.")

        if st.button("View Created Surveys"):
            if admin_password == "casy123":
                conn = sqlite3.connect("app_data.db")
                c = conn.cursor()
                c.execute("SELECT survey_name, survey_code, creator_username, creation_date FROM surveys")
                rows = c.fetchall()
                conn.close()

                if rows:
                    st.subheader("Created Surveys")
                    for row in rows:
                        st.write(f"Survey Name: {row[0]}, Survey Code: {row[1]}, Created By: {row[2]}, Creation Date: {row[3]}")
                else:
                    st.write("No created survey found.")
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
            conn = sqlite3.connect("app_data.db")
            c = conn.cursor()
            c.execute("""
                INSERT INTO users (name, surname, company, username, password)
                VALUES (?, ?, ?, ?, ?)
            """, (name, surname, company, username, password))
            conn.commit()
            conn.close()
            return True, "Account created successfully!"
        except sqlite3.IntegrityError:
            return False, "Username already exists. Please use a different username."

    def log_in(self, username: str, password: str) -> Tuple[bool, str]:
        if not username:
            return False, "Username cannot be empty."
        try:
            conn = sqlite3.connect("app_data.db")
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = c.fetchone()
            conn.close()
            if result is None:
                return False, "Username does not exist. Please sign up first."
            if result[0] != password:
                return False, "Incorrect password. Please try again."
            return True, "Login successful!"
        except Exception as e:
            return False, f"An error occurred: {e}"