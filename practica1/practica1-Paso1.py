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


# n = number of nodes
# m = number of edges
# 
def remove_leaves(G, X, Y, Z):
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


remove_leaves(G,"A","B",set(["C"]))
nx.draw(G, with_labels=True)
plt.show()