import math

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



def obtener_grafo(pesos,variables):
    return None






