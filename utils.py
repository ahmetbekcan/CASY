import streamlit as st

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