from chow_liu import *
import random 


def generar_nombres(num):
    nombres = []
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    while len(nombres) < num:
        n = len(nombres)
        nombre = ""

        while True:
            nombre = alfabeto[n % 26] + nombre
            n = n // 26 - 1
            if n < 0:
                break

        nombres.append(nombre)

    return nombres

def crear_variables(numVariables,maxCardinalidad):
    nombres = generar_nombres(numVariables)
    for nombre in nombres: 
        variables.append(Variable(nombre,random.randint(2,maxCardinalidad)))
        
    return variables


def numeros_suman_uno(n):
    numeros = [random.random() for _ in range(n)]  
    total = sum(numeros)             
    return [x / total for x in numeros]


def crear_tabla(variables):
    tabla = {}

    for var in variables:
        nombre = var.get_nombre()
        valores = numeros_suman_uno(var.get_cardinalidad())
        for i in range(var.get_cardinalidad()):
            tabla[frozenset({(nombre,i)})] = valores[i]

    for i in range(len(variables)):
        nombreI = variables[i].get_nombre()
        cardinalidadI = variables[i].get_cardinalidad()
        for j in range(i + 1, len(variables)):
            nombreJ = variables[j].get_nombre()
            cardinalidadJ = variables[j].get_cardinalidad()
            valores = numeros_suman_uno(cardinalidadI * cardinalidadJ)
            for valor1 in range(cardinalidadI):
                for valor2 in range(cardinalidadJ):
                    tabla[frozenset({(nombreI,valor1),(nombreJ,valor2)})] = valores[valor1 * cardinalidadJ + valor2]

    return tabla


if __name__ == "__main__":
    variables = crear_variables(10,2)
    tablas = crear_tabla(variables)

    pesos = obtener_pesos(variables, tablas)
    print("----------------------------------------------------------------------")
    print("Pesos de las aristas entre nodos del grafo ordenados de mayor a menor:")
    print("----------------------------------------------------------------------")
    print(pesos)
 
    grafo = obtener_arbol(pesos, variables)
    grafo2 = obtener_arbol_conjuntos(pesos, variables)

    print("----------------------------------------------------------------------")
    print("Mostrando grafos iniciales con pesos")
    print("----------------------------------------------------------------------")

    plt.figure(figsize=(10, 5))  
    plt.subplot(1, 2, 1)
    pos1 = nx.spring_layout(grafo, k=3)  
    nx.draw(grafo, pos1, with_labels=True, node_color="lightblue", node_size=1000)
    labels = {(u, v): f"{w.get('weight', 0):.2f}" for u, v, w in grafo.edges(data=True)}
    nx.draw_networkx_edge_labels(grafo, pos1, edge_labels=labels, font_size=6)
    plt.title("En profundidad")

    plt.subplot(1, 2, 2)
    pos2 = nx.spring_layout(grafo2, k=3)
    nx.draw(grafo2, pos2, with_labels=True, node_color="lightgreen", node_size=1000)
    labels2 = {(u, v): f"{w.get('weight', 0):.2f}" for u, v, w in grafo.edges(data=True)}
    nx.draw_networkx_edge_labels(grafo2, pos2, edge_labels=labels2, font_size=6)
    plt.title("Conjuntos")

    plt.show()
    
    print("----------------------------------------------------------------------")
    print("Mostrando grafos tras aplicar el algoritmo de Chow-Liu")
    print("----------------------------------------------------------------------")
    print("Arbol en profundidad:")
    dir_arbol = asignar_direccionalidad(grafo)
    print("Arbol conjuntos:")
    dir_arbol2 = asignar_direccionalidad(grafo2)
    print("----------------------------------------------------------------------")
    # quiero plotear el grafo de nuevo
    pos = nx.spring_layout(dir_arbol, k=3)
    pos2 = nx.spring_layout(dir_arbol2, k=3)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    nx.draw(dir_arbol, pos, with_labels=True, node_color="lightblue", node_size=1000)
    labels = nx.get_edge_attributes(dir_arbol, 'weight')
    nx.draw_networkx_edge_labels(dir_arbol, pos, edge_labels=labels)
    plt.title("Grafo resultante en profundidad")

    plt.subplot(1, 2, 2)
    nx.draw(dir_arbol2, pos2, with_labels=True, node_color="lightgreen", node_size=1000)
    labels2 = nx.get_edge_attributes(dir_arbol2, 'weight')
    nx.draw_networkx_edge_labels(dir_arbol2, pos2, edge_labels=labels2)
    plt.title("Grafo resultante conjuntos")
    plt.show()
