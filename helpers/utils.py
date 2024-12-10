import streamlit as st
from database.database_wrapper import DatabaseWrapper

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return ""
    
def render_logo(logo_path="ui_components/logo.PNG"):
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(logo_path,width=100)

def initialize_database():
    db = DatabaseWrapper()
    try:
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                company TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.execute_query("""
            CREATE TABLE IF NOT EXISTS survey_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_name TEXT NOT NULL,
                session_code TEXT UNIQUE NOT NULL,
                creator_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)

        db.execute_query("""
            CREATE TABLE IF NOT EXISTS surveys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                participant_id INTEGER NOT NULL, 
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_completed BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (participant_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (session_id) REFERENCES survey_sessions (id) ON DELETE CASCADE
            )
        """)

        db.execute_query("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                survey_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (survey_id) REFERENCES surveys (id) ON DELETE CASCADE
            )
        """)

        db.execute_query("""
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                response_text TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE
            )
        """)
    except Exception as e:
        print(f"Error initializing database: {e}")

    db.close()

#Always log after appending latest message!!
def log_chat_input():
    role = st.session_state.messages[-1]["role"]
    message = st.session_state.messages[-1]["content"]
    get_current_survey_id()
    if (st.session_state.cached_survey_id == None):
        return
    
    db = DatabaseWrapper()

    if (role == "assistant"):
        db.execute_query("""
                        INSERT INTO questions (survey_id, question_text) 
                        VALUES (?, ?);
                        """, (st.session_state.cached_survey_id, message))
    elif (role == "user"):
        question_id = db.fetch_one("""
                        SELECT id AS question_id
                        FROM questions
                        WHERE survey_id = ?
                        ORDER BY created_at DESC
                        LIMIT 1;
                        """, (st.session_state.cached_survey_id,))
        if question_id:
            db.execute_query("""
                            INSERT INTO responses (question_id, response_text)
                            VALUES (?, ?);
                            """, (question_id[0], message))

    db.close()

def get_current_survey_id():
    if (not st.session_state.cached_survey_id == None):
        return
    if (st.session_state.joined_survey_session_code == None):
        return None
    if (st.session_state.username == ""):
        return None
    
    db = DatabaseWrapper()
    survey_id = db.fetch_one("""
                SELECT surveys.id AS survey_id
                FROM surveys
                JOIN survey_sessions ON surveys.session_id = survey_sessions.id
                JOIN users ON surveys.participant_id = users.id
                WHERE survey_sessions.session_code = ? AND users.username = ?;
                """, (st.session_state.joined_survey_session_code, st.session_state.username))
    db.close()
    
    if (survey_id):
        st.session_state.cached_survey_id = survey_id[0]

def get_participant_and_session_id():
    if (st.session_state.cached_participant_id and st.session_state.cached_survey_session_id):
        return
    db = DatabaseWrapper()
    
    result = db.fetch_one("""
                SELECT users.id AS participant_id, survey_sessions.id AS session_id
                FROM users
                JOIN survey_sessions ON survey_sessions.session_code = ?
                WHERE users.username = ?;
            """, (st.session_state.joined_survey_session_code, st.session_state.username))
    
    if (result):
        st.session_state.cached_participant_id, st.session_state.cached_survey_session_id = result
    db.close()

def log_survey():
    get_participant_and_session_id()
    if (not st.session_state.cached_participant_id and not st.session_state.cached_survey_session_id):
        return
    
    db = DatabaseWrapper()
    db.execute_query("""
                INSERT INTO surveys (session_id, participant_id) 
                VALUES (?, ?);
                """, (st.session_state.cached_survey_session_id, st.session_state.cached_participant_id))
    db.close()

def get_completed_surveys():
    db = DatabaseWrapper()
    
    completed_surveys = db.fetch_all("""
                                        SELECT surveys.id AS survey_id, survey_sessions.session_name, survey_sessions.session_code, surveys.created_at
                                        FROM surveys
                                        JOIN survey_sessions ON surveys.session_id = survey_sessions.id
                                        WHERE survey_sessions.creator_id = (SELECT id FROM users WHERE username = ?)
                                        AND surveys.is_completed = TRUE;
                                    """, (st.session_state.username,))
    db.close()
    
    return completed_surveys

def clear_cached_values():
    st.session_state.cached_survey_session_id = None
    st.session_state.cached_participant_id = None
    st.session_state.cached_survey_id = None