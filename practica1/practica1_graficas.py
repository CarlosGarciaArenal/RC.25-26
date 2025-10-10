from practica1_Paso1 import remove_leaves
from practica1_Paso2 import joinAndIgnore
from practica1_Paso3 import quitar_Z, existen_caminos
import networkx as nx
import matplotlib.pyplot as plt
import time


def crearGrafoNoDirigioCompleto(n):
    G = nx.DiGraph()
    for i in range(n):  
        for j in range(i + 1, n):
            G.add_edge(i, j)                                                                                             
    return G.to_directed()


def graficas_tiempo(numNodos):
    tiempos_paso1 = []
    tiempos_paso2 = []
    tiempos_paso3 = []
    tiempos_totales = []

    G_grande = crearGrafoNoDirigioCompleto(numNodos[-1])
    
    for nodos in numNodos:

        G = G_grande.subgraph(range(nodos)).copy()
        G.add_node(nodos + 1)
        X = {0}
        Y = {nodos + 1}
        Z = set(range(1, nodos - 1))
            
        start_total = time.time()
        remove_leaves(G, X, Y, Z)
        tiempo_paso1 = time.time() - start_total
        
        
        start_paso2 = time.time()
        G = joinAndIgnore(G)
        tiempo_paso2 = time.time() - start_paso2
        
        
        start_paso3 = time.time()
        quitar_Z(G, Z)
        existen_caminos(G, list(X)[0], list(Y)[0])
        tiempo_paso3 = time.time() - start_paso3 
        
        tiempo_total = time.time() - start_total
        
        tiempos_paso1.append(tiempo_paso1)
        tiempos_paso2.append(tiempo_paso2)
        tiempos_paso3.append(tiempo_paso3)
        tiempos_totales.append(tiempo_total)
        
        print(f"Nodos: {nodos} - Total: {tiempo_total:.4f}s")

    fig, axes = plt.subplots(2, 2, figsize=(24, 20))
    
   
    axes[0, 0].plot(numNodos, tiempos_paso1, marker='o', color='blue')
    axes[0, 0].set_xlabel('Total de vértices (n)')
    axes[0, 0].set_ylabel('Tiempo (segundos)')
    axes[0, 0].set_title('Paso 1')
    axes[0, 0].grid(True)
    
    
    axes[0, 1].plot(numNodos, tiempos_paso2, marker='o', color='green')
    axes[0, 1].set_xlabel('Total de vértices (n)')
    axes[0, 1].set_ylabel('Tiempo (segundos)')
    axes[0, 1].set_title('Paso 2')
    axes[0, 1].grid(True)
    
    
    axes[1, 0].plot(numNodos, tiempos_paso3, marker='o', color='red')
    axes[1, 0].set_xlabel('Total de vértices (n)')
    axes[1, 0].set_ylabel('Tiempo (segundos)')
    axes[1, 0].set_title('Paso 3')
    axes[1, 0].grid(True)
    
    
    axes[1, 1].plot(numNodos, tiempos_totales, marker='o', color='purple')
    axes[1, 1].set_xlabel('Total de vértices (n)')
    axes[1, 1].set_ylabel('Tiempo (segundos)')
    axes[1, 1].set_title('Tiempo Total')
    axes[1, 1].grid(True)
    
    
    
    plt.subplots_adjust(hspace=0.3, wspace=0.3)  
    plt.show()


if __name__ == "__main__":
    nodos = [20, 50, 100, 150, 200, 250, 300, 400, 450, 500]
    graficas_tiempo(nodos)
