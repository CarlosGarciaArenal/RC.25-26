import matplotlib.pyplot as plt
import random
from itertools import product
from prueba import *


def crear_lista_variables(numVariables, maxCardinalidad):
    listaVariables = []
    for i in range(0,numVariables):
        listaVariables.append(Variable(i, random.randint(2,maxCardinalidad)))
    
    return listaVariables


def todas_asignaciones_variables(variables):
    asignaciones = []
    rangos = [range(var.get_cardinality()) for var in variables]
    for combinacion in product(*rangos): 
        asignacion = frozenset(
            (variables[i].get_name(), combinacion[i]) for i in range(len(variables))
        )
        asignaciones.append(asignacion)
    return asignaciones


def lista_factores(numFactores,variables,maxVaribales):
    listaFactores = []
    for i in range(numFactores):
        valido = False
        while not valido:
            numVaribales = random.randint(1,maxVaribales)
            nombreVariables = [random.randint(1, maxVaribales) for _ in range(numVaribales)]  
            valido = True
            for factor in listaFactores:
                if set(factor.get_variables()) == set(nombreVariables):
                    valido = False
                    break

            if valido:
                assignaciones = todas_asignaciones_variables(variables)
                listaFactores.append(Factor(assignaciones))

    return listaFactores

if __name__ == "__main__":

    variables = crear_lista_variables(5,4)
    print("Lista de Variables:")
    for var in variables:
        print(var.get_name(), "Cardinalidad:", var.get_cardinality())

    
    lista_factores = lista_factores(3,variables,3)
    print("\nLista de Factores:")   

    for factor in lista_factores:
        factor.show_factor()
    






