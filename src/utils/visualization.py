from pyvis import network
from networkx.classes.graph import Graph

def show_network(network_graph: Graph, filename: str, physics: bool=False) -> None:
    nt = network.Network(width='100%', height='100vh', directed=True)
    nt.from_nx(network_graph)
    nt.toggle_physics(physics)
    nt.show(filename, notebook=False)
