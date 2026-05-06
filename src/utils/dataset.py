import pandas as pd
import streamlit as st
import random

@st.cache_data
def get_raw_transactions(path_to_file:str="src/data/HI-Small_Trans.csv", sample_percentage=None) -> pd.DataFrame:
    if sample_percentage is not None:
        return pd.read_csv(
            path_to_file, 
            skiprows=lambda i: i > 0 and random.random() > sample_percentage)
    return pd.read_csv(path_to_file, engine="pyarrow")