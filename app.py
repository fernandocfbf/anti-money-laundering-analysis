import streamlit as st
import streamlit.components.v1 as components

from src.utils.dataset import get_network_analysis_dataset
from src.network_analysis import NetworkAnalysis, NetworkContext

# 🎨 Configuração da Página
st.set_page_config(
    layout="wide", 
    page_title="AML Analysis"
)
st.markdown(
    "<h1 style='text-align: center;'>Anti-Money Laundering Analysis</h1>", 
    unsafe_allow_html=True
)
transactions_df = get_network_analysis_dataset()
with st.sidebar:
    st.header("Settings")
    selected_account_id = st.selectbox(
        'Choose an Account ID:', 
        sorted(set(transactions_df['sender']))
    )
    max_depth = st.slider("Select Network Depth", min_value=1, max_value=10, value=6)
    max_nodes = st.slider("Select Max Nodes", min_value=10, max_value=300, value=50)
    physics = st.toggle('Enable Physics', value=True)

# 🔍 Gerar análise de rede
network_context = NetworkContext(transactions_df, physics, selected_account_id, max_depth, max_nodes)
network_analysis = NetworkAnalysis(network_context)
network_analysis.generate_network()

# 📡 Exibir o gráfico de rede
st.subheader("Network Visualization")
network_html = open("pyvis_network.html", 'r', encoding='utf-8').read()
st.markdown("---")
st.components.v1.html(network_html, height=500, scrolling=True)
