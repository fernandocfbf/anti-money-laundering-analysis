import json
import streamlit as st

@st.cache_data
def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def get_translator(source_file="src/constants/translate.json"):
    return read_json_file(source_file)