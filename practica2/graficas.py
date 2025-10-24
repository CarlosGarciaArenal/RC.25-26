import matplotlib.pyplot as plt
import random
import time
from itertools import product
from version_itertools import *


def crear_lista_variables_aleatorias(numVariables, maxCardinalidad):
    listaVariables = []
    for i in range(0,numVariables):
        listaVariables.append(Variable(i, random.randint(2,maxCardinalidad)))
    
    return listaVariables


def todas_asignaciones_variables(variables):
    asignaciones = {}
    rangos = [range(var.get_cardinality()) for var in variables]
    for combinacion in product(*rangos): 
        asignacion = frozenset(
            (variables[i].get_name(), combinacion[i]) for i in range(len(variables))
        )
        asignaciones[asignacion] = 0.5
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
                asignaciones = todas_asignaciones_variables(variables)
                listaFactores.append(Factor(asignaciones))
    
    return listaFactores


def crear_lista_variables(numVariables,cardinalidad):
    listaVariables = []
    for i in range(0,numVariables):
        listaVariables.append(Variable(i, cardinalidad))
    return listaVariables

def crear_lista_factores_completos(variables):
    listaFactores = []
    for i in range(len(variables)):
        lista_aux = variables[:i + 1]
        asignaciones = todas_asignaciones_variables(lista_aux)
        listaFactores.append(Factor(asignaciones, lista_aux))
    return listaFactores


def crear_lista_factores_fila(variables):
    listaFactores = []
    for i in range(len(variables)):
        lista_aux = variables[i:i + 1]
        asignaciones = todas_asignaciones_variables(lista_aux)
        listaFactores.append(Factor(asignaciones, lista_aux))
    return listaFactores

if __name__ == "__main__":

    numero_variables = 14
    listaVariables = crear_lista_variables(numero_variables,3)  
    num_factores = [f for f in range(3, numero_variables + 1)]
    tiempos_itertools = []
    for n in num_factores:
        lista_factores_aux = crear_lista_factores_completos(listaVariables[:n])
        numerator_order = listaVariables[1:n-1]
        denominator_order = listaVariables[n-1:n]
        start = time.time()
        inferencia_condicional_itertools(lista_factores_aux, numerator_order, denominator_order)
        total_time = time.time() - start
        tiempos_itertools.append(total_time)
        print("-----------------------------------")
        print(f"Tiempos para {n} factores (itertools): {total_time} segundos")
        print("-----------------------------------")


    plt.plot(range(len(tiempos_itertools)), tiempos_itertools)
    plt.xticks(range(len(tiempos_itertools)), num_factores)
    plt.xlabel("Número de factores")
    plt.ylabel("Tiempo (s)")
    plt.title("Tiempos de inferencia condicional (itertools)")
    plt.show()

       