from practica1_Paso1 import remove_leaves
from practica1_Paso2 import joinAndIgnore
from practica1_Paso3 import quitar_Z,existen_caminos
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

nodes = ["A", "B", "C", "D", "E", "F"]
edges = [("A", "C"), ("B", "C"), ("C", "D"),
         ("C", "E"), ("D", "F"), ("E", "F")]

X = "A"
Y = "E"
Z = set(["B"])

def prueba(G, nodes, edges, X, Y, Z):
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Paso 1
    remove_leaves(G, X, Y, Z)
    print("Nodos tras eliminar hojas:", G.nodes())
    print("Aristas tras eliminar hojas:", G.edges())

    # Paso 2
    G = joinAndIgnore(G)
    print("Nodos tras hacer no dirigido y unir padres con hijos en comun:", G.nodes())
    print("Aristas tras hacer no dirigido y unir padres con hijos en comun:", G.edges())

    # Paso 3
    quitar_Z(G, Z)
    print("Nodos tras quitar Z:", G.nodes())
    print("Aristas tras quitar Z:", G.edges())

    # Comprobar si hay caminos entre nodos de X e Y
    resultado = existen_caminos(G,X,Y)
    if resultado:
        print(f"Existe un camino entre {X} e {Y}")
    else:
        print(f"No existe un camino entre {X} e {Y}")             

prueba(G, nodes, edges, X, Y, Z)