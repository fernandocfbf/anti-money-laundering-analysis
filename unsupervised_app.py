import streamlit as st

# personalized modules
from src.utils.dataset import get_raw_transactions

#constants
DATA_PATH = f"src\\data\\output\\raw_transactions.csv"

st.set_page_config(
    layout="wide", 
    page_title="AML Analysis"
)
'''raw_df = get_raw_transactions(DATA_PATH)
raw_df = raw_df.sample(n=1000)

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.title("Anti Money Laundering Analysis")
    st.dataframe(raw_df, use_container_width=True)'''

