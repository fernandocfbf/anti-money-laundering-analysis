import streamlit as st

from src.utils.dataset import get_network_analysis_dataset, get_full_transactions_dataset, get_accounts_details_dataset
from src.network_analysis import NetworkAnalysis, NetworkContext
from src.profile_analysis import ProfileAnalysis, ProfileContext

st.set_page_config(
    layout="wide", 
    page_title="AML Analysis"
)

st.markdown(
    "<h1 style='text-align: center;'>Anti-Money Laundering Analysis</h1>", 
    unsafe_allow_html=True
)
st.markdown("---")
accounts_details = get_accounts_details_dataset()
full_transactions_dataframe = get_full_transactions_dataset(visualization=True)

with st.sidebar:
    st.header("Analysis Filters")
    account_id = st.selectbox(
        'Choose an Account ID:', 
        sorted(set(accounts_details['account_id']))
    )
    st.header("Account Details")

profile_context = ProfileContext(accounts_details, full_transactions_dataframe, account_id)
profile_analysis = ProfileAnalysis(profile_context)

with st.sidebar:
    profile_analysis.generate_profile_overview()

profile_analysis.generate_metrics()
st.markdown("")
timeline_col, pie_col = st.columns([8,4])
with timeline_col:
    profile_analysis.generate_transactions_timeline_chart()
    profile_analysis.generate_dataframe_overview()
with pie_col:
    profile_analysis.generate_payment_method_pie_chart()
    profile_analysis.generate_transactions_distribuition()

st.header("Network Analysis")
st.markdown("---")
col1, col2, col3 = st.columns(3)
max_depth = col1.slider("Select Network Depth", min_value=1, max_value=10, value=3)
max_nodes = col2.slider("Select Max Nodes", min_value=10, max_value=300, value=50)
physics = col3.toggle('Enable Physics', value=True)

network_dataframe = get_network_analysis_dataset(full_transactions_dataframe)
network_context = NetworkContext(network_dataframe, physics, account_id, max_depth, max_nodes)
network_analysis = NetworkAnalysis(network_context)
network_analysis.generate_network()
network_html = open("pyvis_network.html", 'r', encoding='utf-8').read() 
st.components.v1.html(network_html, height=600, scrolling=False)


