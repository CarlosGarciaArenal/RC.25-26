import networkx as nx

G1 = nx.DiGraph()
nodes = ["A", "B", "C", "D"]
edges = [("A", "B"), ("A", "D"), ("D", "C")]
G1.add_nodes_from(nodes)
G1.add_edges_from(edges)

G2 = nx.DiGraph()
nodes = ["A"]
edges = []
G2.add_nodes_from(nodes)
G2.add_edges_from(edges)

G3 = nx.DiGraph()
nodes = ["A", "B"]
edges = [("A", "B")]
G3.add_nodes_from(nodes)
G3.add_edges_from(edges)

G4 = nx.DiGraph()
nodes = ["A", "B", "C", "D", "E", "F", "H"]
edges = [("A", "B"), ("A", "D"), ("D", "C"), ("D", "E"), ("A", "F"), ("A", "H")]
G4.add_nodes_from(nodes)
G4.add_edges_from(edges)


def asignar_direccionalidad(arbol):
    nodo_elegido = list(arbol.nodes)[0]

    to_explore = set(nodo_elegido)
    explorados = set()

    nuevo_arbol = nx.Graph()
    nuevo_arbol.add_node(nodo_elegido)

    while to_explore:
        current = to_explore.pop()
        neighbours = list(nx.neighbors(arbol, current))
        to_explore = to_explore.union(set(neighbours))
        explorados.add(current)

        for node in neighbours:
            if node not in list(nuevo_arbol.nodes):
                nuevo_arbol.add_node(node)
            if node not in explorados:
                nuevo_arbol.add_edge(current, node)
    return nuevo_arbol
## La complejidad de asignar_direccionalidad es de O(n*e), donde n es el numero de nodos
## y e el numero de aristas

print(list(asignar_direccionalidad(G4).edges))
