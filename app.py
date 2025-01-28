import streamlit as st
import streamlit.components.v1 as components

import networkx as nx
from pyvis import network

from src.utils.dataset import get_network_analysis_dataset

from src.network_analysis import NetworkAnalysis, NetworkContext

st.set_page_config(page_title="AML Analysis", page_icon="src/images/aml.png")
st.sidebar.title('Anti Money Laudering Analysis')

transactions_df = get_network_analysis_dataset()
selected_account_id = st.sidebar.selectbox('Choose a account ID to analyse:', set(transactions_df['sender']))
max_depth = st.sidebar.number_input("Select network max depth", value=6, placeholder="Type a number...")
max_nodes = st.sidebar.number_input("Select network max nodes", max_value=300, value=50, placeholder="Type a number...")
physics = st.sidebar.checkbox('enable physics', value=True)
network_context = NetworkContext(transactions_df, physics, selected_account_id, max_depth, max_nodes)
network_analysis = NetworkAnalysis(network_context)
network_analysis.generate_network()
network_html = open("pyvis_network.html", 'r', encoding='utf-8').read()
with st.container(height=500):
    components.html(network_html, height=460)