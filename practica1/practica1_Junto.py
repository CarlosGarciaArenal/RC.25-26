from practica1_Paso1 import remove_leaves
from practica1_Paso2 import joinAndIgnore
from practica1_Paso3 import quitar_Z,existen_caminos
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

nodes = ["A", "B", "C", "D", "E", "F"]
edges = [("A", "C"), ("B", "C"), ("C", "D"),
         ("C", "E"), ("D", "F"), ("E", "F")]

edges_ej3 = [("A", "C"), ("C", "D"),
             ("D", "F"), ("B", "E")]

X = "A"
Y = "E"
Z = set(["B"])

def algoritmo_separacion(G, nodes, edges, X, Y, Z):
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    print("Nodos inicialmente:", G.nodes())
    print("Aristas inicialmente:", G.edges())
    print("X:",X,"Y:",Y,"Z:",Z)

    nx.draw(G, with_labels=True)
    plt.show()

    # Paso 1
    remove_leaves(G, X, Y, Z)
    print("Nodos tras eliminar hojas:", G.nodes())
    print("Aristas tras eliminar hojas:", G.edges())

    nx.draw(G, with_labels=True)
    plt.show()

    # Paso 2
    G = joinAndIgnore(G)
    print("Nodos tras hacer no dirigido y unir padres con hijos en comun:", G.nodes())
    print("Aristas tras hacer no dirigido y unir padres con hijos en comun:", G.edges())

    nx.draw(G, with_labels=True)
    plt.show()

    # Paso 3
    quitar_Z(G, Z)
    print("Nodos tras quitar Z:", G.nodes())
    print("Aristas tras quitar Z:", G.edges())

    nx.draw(G, with_labels=True)
    plt.show()

    # Comprobar si hay caminos entre nodos de X e Y
    resultado = existen_caminos(G,X,Y)
    if resultado:
        print(f"Existe un camino entre {X} y {Y}")
        print(f"{X} y {Y} no son separables dados {Z}")
    else:
        print(f"No existe un camino entre {X} y {Y}")
        print(f"{X} y {Y} son separables dados {Z}")      

print("------------------------------------------")
print("Ejemplo 1: existe un camino entre X e Y.")
# En este grafo debería existir un único camino entre X e Y
# en el que no está el nodo E perteneciente a Z. Consecuentemente,
# existen caminos entre X e Y sin ningún Z por lo que no son separables. 
algoritmo_separacion(G, nodes, edges, X, Y, Z)

G.clear()

print("------------------------------------------")
print("Ejemplo 2: Un elemento en Z en el camino entre X e Y.")
# En este grafo debería existir un único camino entre X e Y
# con el nodo C perteneciente a Z entre X e Y. Consecuentemente, no
# existen caminos entre X e Y sin ningún Z por lo que son separables. 
Z = set(["C"])
algoritmo_separacion(G, nodes, edges, X, Y, Z)

G.clear()

print("------------------------------------------")
print("Ejemplo 3: X e Y en componentes conexas distintas.")
# No existe un camino entre X e Y. Consecuentemente, son separables
# independientemente de los nodos en Z.
Z = set()
algoritmo_separacion(G, nodes, edges_ej3, X, Y, Z)

G.clear()

print("------------------------------------------")
print("Ejemplo 4: Dos caminos entre X e Y. Ambos caminos contienen un Z.")
# En este grafo deberían existir dos caminos entre X e Y. D perteneciente
# a Z se encuentra en uno de los caminos y E perteneciente a Z en el otro.
# Consecuentemente, no existen caminos entre X e Y sin ningún Z por lo que 
# son separables. 
X = "A"
Y = "F"
Z = set(["D","E"])
algoritmo_separacion(G, nodes, edges, X, Y, Z)

G.clear()

print("------------------------------------------")
print("Ejemplo 5: Dos caminos entre X e Y. Uno de los caminos contiene un Z.")
# En este grafo deberían existir dos caminos entre X e Y. D perteneciente
# a Z se encuentra en uno de los caminos. El otro camino no contiene ningún Z.
# Consecuentemente, existe al menos un camino entre X e Y sin ningún Z.
# X e Y no son separables al haber al menos un camino libre entre X e Y.
X = "A"
Y = "F"
Z = set(["D"])
algoritmo_separacion(G, nodes, edges, X, Y, Z)
