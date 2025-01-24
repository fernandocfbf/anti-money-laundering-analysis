import pandas as pd
import networkx as nx
from pyvis import network

from src.utils.visualization import generate_network

class NetworkAnalysis:
    def __init__(self, transactions_df: pd.DataFrame, physics: bool):
        self.transactions_df = transactions_df
        self.physics = physics

    def generate_network(self):
        relationship_network = nx.from_pandas_edgelist(self.transactions_df, source="sender", target="receiver", edge_attr=["title","value"])
        degree_dict_G = dict(relationship_network.degree)
        nx.set_node_attributes(relationship_network, degree_dict_G, "value")
        title_dict_G = {}
        for node in list(relationship_network.nodes):
            title_dict_G[node] = f"id: {node}"
        nx.set_node_attributes(relationship_network, title_dict_G, "title")
        generate_network(relationship_network, "pyvis_network.html", physics=self.physics)