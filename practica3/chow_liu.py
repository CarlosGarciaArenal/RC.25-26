import math
import matplotlib.pyplot as plt
import networkx as nx

class Variable:
    def __init__(self, nombre, cardinalidad):
        self.nombre = nombre
        self.cardinalidad = cardinalidad

    def get_nombre(self):
        return self.nombre
    
    def get_cardinalidad(self):
        return self.cardinalidad

tablas = {}

tablas[frozenset({('A',0)})] = 0.5
tablas[frozenset({('A',1)})] = 0.5
tablas[frozenset({('B',0)})] = 0.5
tablas[frozenset({('B',1)})] = 0.5
tablas[frozenset({('C',0)})] = 0.3
tablas[frozenset({('C',1)})] = 0.7

tablas[frozenset({('A',0),('B',0)})] = 0.3
tablas[frozenset({('A',0),('B',1)})] = 0.2
tablas[frozenset({('A',1),('B',0)})] = 0.2
tablas[frozenset({('A',1),('B',1)})] = 0.3

tablas[frozenset({('A',0),('C',0)})] = 0.18
tablas[frozenset({('A',0),('C',1)})] = 0.32
tablas[frozenset({('A',1),('C',0)})] = 0.12
tablas[frozenset({('A',1),('C',1)})] = 0.38

tablas[frozenset({('B',0),('C',0)})] = 0.18
tablas[frozenset({('B',0),('C',1)})] = 0.32
tablas[frozenset({('B',1),('C',0)})] = 0.12
tablas[frozenset({('B',1),('C',1)})] = 0.38


A = Variable('A',2)
B = Variable('B',2)
C = Variable('C',2)

variables = [A,B,C]

# Paso 1: Obtener los pesos de las aristas
def obtener_pesos(variables, tablas):
    pesos = []
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            peso = 0
            for valor1 in range(variables[i].get_cardinalidad()):
                for valor2 in range(variables[j].get_cardinalidad()):
                    llave = frozenset({
                        (variables[i].get_nombre(), valor1),
                        (variables[j].get_nombre(), valor2)
                    })

                    llave1 = frozenset({(variables[i].get_nombre(), valor1)})
                    llave2 = frozenset({(variables[j].get_nombre(), valor2)})

                    peso += tablas[llave] * math.log2(
                        tablas[llave] / (tablas[llave1] * tablas[llave2])
                    )

            pesos.append(({variables[i].get_nombre(),variables[j].get_nombre()},peso))

    pesos.sort(key=lambda x: x[1], reverse=True)

    return pesos

# Paso 2: Obtener el árbol de recubrimiento máximo usando networkx, voy añadiendo las aristas de mayor peso que no forman un ciclo
def obtener_arbol(pesos_ordenados,variables):
    G = nx.Graph()
    # Pongo los nodos en el grafo
    nombres = [var.get_nombre() for var in variables]
    for nombre in nombres:
        G.add_node(nombre)
        # recorro los pesos que están ordenados de mayor a menor peso (facilita las cosas)
    for (vars, peso) in pesos_ordenados:
        nodo1, nodo2 = list(vars)
        # Si uno de los nodos no está en el grafo, no puede haber un ciclo añadiendo la arista
        if not forma_ciclo(nodo1, nodo2, G):
            G.add_edge(nodo1, nodo2, weight=peso)
    # Crear un nuevo grafo solo con las aristas del árbol
    return G

# Función auxiliar para determinar si al añadir una arista se forma un ciclo o no (retorna un booleano)
# es una busqueda en profundidad desde nodo1 hasta nodo2
def forma_ciclo(nodo1, nodo2, grafo):
    visitados = set() # set de visitados
    pila = [nodo1] # pila para la busqueda en profundidad
    encontrado = False # bandera para saber si se encontro el camino
    # La complejidad maxima de esta busqueda es O(n+e) siendo n el numero de nodos y e las aristas
    while pila:
        actual = pila.pop()
        if actual == nodo2:
            encontrado = True
            break
        if actual not in visitados:
            visitados.add(actual)
            vecinos = list(grafo.neighbors(actual))
            for vecino in vecinos:
                if vecino not in visitados:
                    pila.append(vecino)
    return encontrado



def obtener_arbol_conjuntos(pesos_ordenados,variables):
    G = nx.Graph()
    lista_conjuntos = []

    for (vars,_) in pesos_ordenados:
        nodo1,nodo2 = vars
        indice_nodo1 = -1
        indice_nodo2 = -1
        
        for i in range(0,len(lista_conjuntos)):
            if nodo1 in lista_conjuntos[i]:
                indice_nodo1 = i
            if nodo2 in lista_conjuntos[i]:
                indice_nodo2 = i
        if indice_nodo1 < 0 and indice_nodo2 < 0:
            lista_conjuntos.append({nodo1,nodo2})
            G.add_edge(nodo1,nodo2)
        elif indice_nodo1 < 0:
            lista_conjuntos[indice_nodo2].update({nodo1})
            G.add_edge(nodo1,nodo2)
        elif indice_nodo2 < 0:
            lista_conjuntos[indice_nodo1].update({nodo2})
            G.add_edge(nodo1,nodo2)
        elif indice_nodo2 != indice_nodo1:
            lista_conjuntos[indice_nodo2].update(lista_conjuntos[indice_nodo1])
            lista_conjuntos.pop(indice_nodo1)
            G.add_edge(nodo1,nodo2)
        else:
            continue

        if(len(variables) == G.number_of_edges() + 1):
            break
    
    return G

# Paso 3: Asignar direccionalidad al árbol
def asignar_direccionalidad(arbol):
    if not arbol.nodes:
        return nx.DiGraph()
    
    nodo_raiz = list(arbol.nodes)[0]
    print(str(list(arbol.nodes)) + " Nodo escogido para asignar la direccionalidad: " + str(nodo_raiz))
    
    arbol_dirigido = nx.DiGraph()
    
    cola = [nodo_raiz]
    visitados = {nodo_raiz}
    
    arbol_dirigido.add_node(nodo_raiz)
    # otra busqueda en anchura para asignar direccionalidad
    while cola:
        nodo_actual = cola.pop(0)
        for vecino in arbol.neighbors(nodo_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
                arbol_dirigido.add_edge(nodo_actual, vecino)
    return arbol_dirigido