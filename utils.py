import streamlit as st
import sqlite3

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    
def render_logo(logo_path="ui_components/logo.PNG"):
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(logo_path,width=100)

def initialize_database():
    conn = sqlite3.connect("app_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            company TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    c.execute("""
            CREATE TABLE IF NOT EXISTS surveys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                survey_name TEXT NOT NULL,
                survey_code TEXT UNIQUE NOT NULL,
                creator_username TEXT NOT NULL,
                creation_date TEXT NOT NULL
            )
        """)
    
    conn.commit()
    conn.close()