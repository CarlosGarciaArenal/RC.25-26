import networkx as nx
import matplotlib.pyplot as plt

def remove_leaves(G, X, Y, Z):
    check_set = Z.union(X, Y)
    to_explore = set(G.nodes) # Conjunto de nodos a explorar
    while to_explore:
        node = to_explore.pop()
        # Si el nodo no es X ni Y, no pertenece a Z y no tiene sucesores
        if not any(G.successors(node)) and node not in check_set:
            # Actualizamos el conjunto de nodos a explorar con los padres
            # del nodo hoja. Eliminamos el nodo hoja.
            predecessors = list(G.predecessors(node))
            G.remove_node(node)
            to_explore.update(predecessors)

G = nx.DiGraph()
nodes = ["A", "B", "C", "D", "E", "F"]
edges = [("A", "C"), ("B", "C"), ("C", "D"),
         ("C", "E"), ("D", "F"), ("E", "F")]

G.add_nodes_from(nodes)
G.add_edges_from(edges)
nx.draw(G, with_labels=True)
plt.show()

remove_leaves(G,"A","B",set(["C"]))

nx.draw(G, with_labels=True)
plt.show()