from pyvis import network
import streamlit as st
from networkx.classes.graph import Graph

def generate_network_vis(network_graph: Graph, filename: str, physics: bool=False) -> None:
    nt = network.Network(directed=True)
    nt.from_nx(network_graph)
    nt.toggle_physics(physics)
    nt.save_graph(filename)

def generate_info_card(title, value):
    """
    Display a styled information card with a title and highlighted value.
    """
    card_html = f"""
    <div style="
        background-color: #FFFFFF; 
        padding: 5px 15px; 
        border-radius: 8px; 
        width: 100%;
    ">
        <h4 style="margin: 3px 0; color: #555; font-size: 14px;">{title}</h4>
        <p style="margin: 0; font-size: 14px; font-weight: bold; color: #007BFF;">{value}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
