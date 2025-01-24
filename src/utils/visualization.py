from pyvis import network
from networkx.classes.graph import Graph

def generate_network(network_graph: Graph, filename: str, physics: bool=False) -> None:
    nt = network.Network(directed=True)
    nt.from_nx(network_graph)
    nt.toggle_physics(physics)
    nt.save_graph(filename)
