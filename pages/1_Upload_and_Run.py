import streamlit as st
import pandas as pd

# personalized modules
from src.utils.dataset import get_raw_transactions

#constants
DATA_PATH = f"src\\data\\output\\raw_transactions.csv"

st.set_page_config(
    layout="wide", 
    page_title="AML Analysis"
)

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.title("AML Transaction Scoring")
    st.caption("Upload your data or try a demo to see how it works")

with col_center:
    options = ["Use My Data", "Try Demo"]
    selection = st.segmented_control(
        label="", 
        options=options, 
        selection_mode="single",
        width="stretch",
        default="Use My Data")

raw_data = None
if selection == "Use My Data":
    uploaded_file = st.file_uploader(
        "Upload your transactions CSV",
        type=["csv"]
    )

    if uploaded_file:
        raw_data = pd.read_csv(uploaded_file)

elif selection == "Try Demo":
    st.info("Using sample dataset for demonstration.")

    raw_data = get_raw_transactions(DATA_PATH)

if raw_data is not None:
    st.dataframe(raw_data.head(1000), use_container_width=True, height=200)

run_disabled = True if raw_data is None else False
if st.button("Run Model", disabled=run_disabled):
    st.success("C completed!")