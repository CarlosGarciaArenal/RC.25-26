import networkx as nx
import matplotlib.pyplot as plt

# Recorrer los nodos, unir los padres que comparten hijos y hacer el grafo no dirigido

def joinAndIgnore(G):
    newGraph = nx.Graph()
    newGraph.add_nodes_from(G.nodes())
    for v in G.nodes():
        parents = list(G.predecessors(v))
        for p in parents:
            newGraph.add_edge(v,p)
        for i in range(len(parents)):
            for j in range(i+1, len(parents)):
                newGraph.add_edge(parents[i], parents[j])
    return newGraph


if __name__ == "__main__":
    G = nx.DiGraph()
    elist = [("A", "C"), ("B", "C"), ("C", "E"), ("E", "F"), ("C", "D"), ("D", "F"), ("I", "C")]
    G.add_edges_from(elist)

    nx.draw(G, with_labels=True, node_color="lightblue", node_size=2000, font_size=14)
    plt.show()

    G = joinAndIgnore(G)
    nx.draw(G, with_labels=True, node_color="lightblue", node_size=2000, font_size=14)
    plt.show()

