import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
nodes = ["A", "B", "C", "D", "E", "F"]
edges = [("A", "C"), ("B", "C"), ("C", "D"),
         ("C", "E"), ("D", "F"), ("E", "F")]
G.add_nodes_from(nodes)
G.add_edges_from(edges)

#nx.draw(G, with_labels=True)
#plt.show()

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


######################
#########OLD##########
######################
# n = number of nodes
# m = number of edges
def remove_leaves_old(G, X, Y, Z):
   check_set = Z.union(X,Y) 
   to_explore = list(G.nodes) # O(n)
   while to_explore: # O(2n) -> O(n)
        node = to_explore.pop() 
        if len(list(G.successors(node))) == 0 and node not in check_set: #O(n)
            for ele in G.predecessors(node): #O(n - 1) -> O(n)
                if ele not in to_explore:
                    to_explore.append(ele)
            G.remove_node(node) #O(m)

# (O(n) + O(n)) * (O(n) + O(n) + O(m)) = O(n*(n+m))

######################

remove_leaves(G,"A","B",set(["C"]))
nx.draw(G, with_labels=True)
plt.show()