from chow_liu import *
import random 

def crear_variables(numVaribales,maxCardinalidad):
    variables = []
    for i in range(0, numVaribales):
        nombre = chr(65 + i) 
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
    print(pesos)
 
    grafo = obtener_arbol(pesos, variables)
    grafo2 = obtener_arbol_conjuntos(pesos, variables)

    plt.figure(figsize=(10, 5))  
    plt.subplot(1, 2, 1)
    pos1 = nx.spring_layout(grafo)  
    nx.draw(grafo, pos1, with_labels=True, node_color="lightblue", node_size=1000)
    plt.title("En profundidad")

    plt.subplot(1, 2, 2)
    pos2 = nx.spring_layout(grafo2)
    nx.draw(grafo2, pos2, with_labels=True, node_color="lightgreen", node_size=1000)
    plt.title("Conjuntos")

    plt.show()

    dir_arbol = asignar_direccionalidad(grafo)
    # quiero plotear el grafo de nuevo
    pos = nx.spring_layout(dir_arbol)
    nx.draw(dir_arbol, pos, with_labels=True)
    labels = nx.get_edge_attributes(dir_arbol, 'weight')
    nx.draw_networkx_edge_labels(dir_arbol, pos, edge_labels=labels)
    plt.show()
