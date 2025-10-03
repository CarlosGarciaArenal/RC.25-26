import networkx as nx
import matplotlib.pyplot as plt

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

G = nx.DiGraph()
elist = [("A", "C"), ("B", "C"), ("C", "E"), ("E", "F"), ("C", "D"), ("D", "F"), ("I", "C")]
G.add_edges_from(elist)

nx.draw(G, with_labels=True, node_color="lightblue", node_size=2000, font_size=14)
plt.show()

G = joinAndIgnore(G)
nx.draw(G, with_labels=True, node_color="lightblue", node_size=2000, font_size=14)
plt.show()





#######################################################
### PASO 2 ES HACER QUE EL GRAFO SEA NO DIRIGIDO Y
### UNIR PADRES CON HIJOS EN COMUN
########################################################

## Recibe el grafo
# Recorre todos los vertices del grafo. Para cada vertice mira si varios
# varios nodos conectan hacia el en esa direccion (solo aristas direccionadas), si lo hacen crea 
# un enlace no dirigido entre esos nodos (padres)


# habra que mirar is es los dos que son predecessors, ya son predecessors y sucessors entre ellos
# Primero uno los predecessor y luego recorro de nuevo y lo paso a no dirigido
