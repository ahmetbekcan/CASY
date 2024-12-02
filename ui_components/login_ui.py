import streamlit as st
import sqlite3
from typing import Tuple
from utils import render_logo

# Initialize the database
def initialize_database():
    conn = sqlite3.connect("app_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            company TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

class LoginUI:
    def render(self):
        render_logo()
        st.title("Welcome to CASY!",)
        tab1, tab2, tab3 = st.tabs(["Log In", "Sign Up", "Admin View"])
        with tab1:
            self.render_log_in()
        with tab2:
            self.render_sign_up()
        with tab3:
            self.render_admin_view()

    def render_sign_up(self):
        st.header("Sign Up")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        name = st.text_input("Name", key="signup_name")
        surname = st.text_input("Surname", key="signup_surname")
        company = st.text_input("Current/Most Recent Company", key="signup_company")

        if st.button("Sign Up"):
            success, message = self.sign_up_user(name, surname, company, email, password)
            if success:
                st.success(message)
            else:
                st.error(message)

    def render_log_in(self):
        st.header("Log In")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Log In"):
            success, message = self.log_in(email, password)
            if success:
                st.success(message)
                st.write(f"Welcome back, {email}!")
                st.session_state.logged_in = True
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
                c.execute("SELECT name, surname, company, email FROM users")
                rows = c.fetchall()
                conn.close()

                if rows:
                    st.subheader("Registered Users")
                    for row in rows:
                        st.write(f"Name: {row[0]}, Surname: {row[1]}, Company: {row[2]}, Email: {row[3]}")
                else:
                    st.write("No registered users found.")
            else:
                st.error("Incorrect admin password.")

    def sign_up_user(self, name: str, surname: str, company: str, email: str, password: str) -> Tuple[bool, str]:
        if not name or not surname:
            return False, "Name and Surname cannot be empty."
        if not company:
            return False, "Company name cannot be empty."
        if not email:
            return False, "Email cannot be empty."
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        try:
            conn = sqlite3.connect("app_data.db")
            c = conn.cursor()
            c.execute("""
                INSERT INTO users (name, surname, company, email, password)
                VALUES (?, ?, ?, ?, ?)
            """, (name, surname, company, email, password))
            conn.commit()
            conn.close()
            return True, "Account created successfully!"
        except sqlite3.IntegrityError:
            return False, "Email already exists. Please use a different email."

    def log_in(self, email: str, password: str) -> Tuple[bool, str]:
        if not email:
            return False, "Email cannot be empty."
        try:
            conn = sqlite3.connect("app_data.db")
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE email = ?", (email,))
            result = c.fetchone()
            conn.close()
            if result is None:
                return False, "Email does not exist. Please sign up first."
            if result[0] != password:
                return False, "Incorrect password. Please try again."
            return True, "Login successful!"
        except Exception as e:
            return False, f"An error occurred: {e}"

if __name__ == "__main__":
    initialize_database()
    login_ui = LoginUI()
    login_ui.render()
