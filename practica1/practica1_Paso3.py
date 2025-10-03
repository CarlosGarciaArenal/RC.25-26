import networkx as nx
import matplotlib.pyplot as plt

def existen_caminos(G,nodo1,nodo2):
    return existen_caminos_aux(G, nodo1, nodo2, [nodo1])

def existen_caminos_aux(G,nodo1,nodo2,visitados):
    vecinos1 = list(G.neighbors(nodo1))
    for vecino in vecinos1:
        if vecino == nodo2:
            return True
        if vecino not in visitados:
            visitados.append(vecino)
            if existen_caminos_aux(G, vecino, nodo2,visitados):
                return True
    return False


def quitar_Z(G,Z):
    for nodo in Z:
        G.remove_node(nodo)



G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5])
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5)])
Z = [3, 5]
quitar_Z(G,Z)
print(G.nodes())
print(G.edges())

#######################################################
### PASO 3 CONSISTE EN QUITAR LOS NODOS DE Z Y
### COMPROBAR SI HAY CAMINOS LOS NODOS
########################################################

# Pimero quito los nodos de Z del grafo
# Despues examina si algun vecino del nodo1 es el nodo2
# Si no es asi, mira los vecinos de los vecinos y asi sucesivamente
# La complejidad temporal es O(E + V) ya que el peor caso es basicamente visitar 
# todos los nodos "E" y todas las aristas "V".