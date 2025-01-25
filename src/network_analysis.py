import logging
logging.basicConfig(level=logging.INFO)

import pandas as pd
import networkx as nx
from dataclasses import dataclass

from src.utils.visualization import generate_network

@dataclass
class NetworkContext:
    transactions_df: pd.DataFrame
    physics: bool
    account_id: int
    max_depth: int
    max_nodes: int

class NetworkAnalysis:
    def __init__(self, network_context: NetworkContext):
        self.network_context = network_context

    def _get_network_by_max_nodes(self, depths):
        limited_nodes = set()
        for i, node in enumerate(depths.keys()):
            if i >= self.network_context.max_nodes:
                break
            limited_nodes.add(node)
        return limited_nodes
    
    def generate_network(self):
        logging.info("Generating accounts network relationships.")
        relationship_network = nx.from_pandas_edgelist(
            self.network_context.transactions_df, 
            source="sender", 
            target="receiver", 
            edge_attr=["title","value"])
        
        logging.info("Setting node attributes.")
        degree_dict_G = dict(relationship_network.degree)
        nx.set_node_attributes(relationship_network, degree_dict_G, "value")
        title_dict_G, color_dict_G  = {}, {}
        for node in list(relationship_network.nodes):
            title_dict_G[node] = f"id: {node}"
            if node == self.network_context.account_id:
                color_dict_G[node] = "#4B0082"
            else:
                color_dict_G[node] = "#EF9900"
        nx.set_node_attributes(relationship_network, title_dict_G, "title")
        nx.set_node_attributes(relationship_network, color_dict_G, "color")

        logging.info(f"Finding filtered network based on account id {self.network_context.account_id} and max depth {self.network_context.max_depth}")
        depths = nx.single_source_shortest_path_length(relationship_network, source=self.network_context.account_id, cutoff=self.network_context.max_depth)
        nodes = self._get_network_by_max_nodes(depths)
        subgraph = relationship_network.subgraph(nodes)
        logging.info("Creating network file (HTML).")
        generate_network(subgraph, "pyvis_network.html", physics=self.network_context.physics)
        logging.info("File created successfully.")