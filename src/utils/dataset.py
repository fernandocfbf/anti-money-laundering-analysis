import pandas as pd
import streamlit as st
        
@st.cache_data
def get_full_transactions_dataset(visualization=False) -> pd.DataFrame:
    dataframe = pd.read_csv("src/data/full_transactions_data.csv")
    if visualization:
        return dataframe.drop(columns=["is_laundering"])
    return dataframe

@st.cache_data
def get_accounts_details_dataset(sample: int=100) -> pd.DataFrame:
    return pd.read_csv("src/data/accounts_details.csv").head(sample)

@st.cache_data
def get_network_analysis_dataset(transactions_df: pd.DataFrame) -> pd.DataFrame:
    network_df = transactions_df.copy()
    network_df = network_df.groupby(["sender", "receiver"], as_index=False).agg({"amount_paid":  "sum"})
    network_df.columns = ['sender','receiver','sum']
    network_df = network_df.rename(columns={"sum": "value"})
    network_df["title"] = network_df.apply(lambda df: f"from: {df.sender}\nto: {df.receiver}\namount (BRL): {df.value}", axis=1)
    return network_df