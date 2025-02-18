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
        background-color: #f8f9fa; 
        padding: 3px 15px; 
        width: 100%;
    ">
        <h4 style="font-size: 14px;">{title}</h4>
        <p style="font-size: 16px; font-weight: bold;">{value}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def generate_metric_card(title: str, value: float):
    st.markdown(
        f"""
        <div style="
            background-color: #FFFFFF;
            padding: 20px; 
        ">
            <p style="margin: 0; font-size: 16px; color: #333;">{title}</p>
            <p style="margin: 5px 0 0; font-size: 32px; color: black;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
