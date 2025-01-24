import streamlit as st
import streamlit.components.v1 as components

import networkx as nx
from pyvis import network

from src.utils.dataset import get_dataset
from src.utils.visualization import generate_network

from src.network_analysis import NetworkAnalysis
from src.transactions import Transactions

st.set_page_config(page_title="AML Analysis", page_icon="src/images/aml.png")
st.sidebar.title('Anti Money Laudering Analysis')

transactions_df = Transactions().load_data()
st.sidebar.date_input(label="Period of analysis", format="DD/MM/YYYY", )
selected_customer = st.sidebar.selectbox('Choose a customer ID to analyse:', set(transactions_df['sender']))
physics=st.sidebar.checkbox('enable physics', value=True)

customer_transactions = transactions_df.query("sender == @selected_customer or receiver == @selected_customer")
network_analysis = NetworkAnalysis(customer_transactions, physics)
network_analysis.generate_network()
network_html = open("pyvis_network.html", 'r', encoding='utf-8').read()
components.html(network_html, height=600, width=800)