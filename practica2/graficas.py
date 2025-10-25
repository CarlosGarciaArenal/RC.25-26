import matplotlib.pyplot as plt
import random
import time
from itertools import product
from version_itertools import *
from enum import Enum


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


def crear_lista_factores_prueba_orden(fila1,fila2):
    listaFactores = []
    for var in fila1:
        lista_aux = [var]
        asignaciones = todas_asignaciones_variables(lista_aux)
        listaFactores.append(Factor(asignaciones, lista_aux))

    var_aux = [fila2[0]]
    var_aux.extend(fila1)
    listaFactores.append(
        Factor(
            todas_asignaciones_variables(var_aux),
            var_aux))

    for i in range(len(fila2) - 1):
        lista_aux = fila2[i:i + 2]
        lista_aux.extend(fila1)
        asignaciones = todas_asignaciones_variables(lista_aux)
        listaFactores.append(Factor(asignaciones, lista_aux))
    return listaFactores

if __name__ == "__main__":

    pruebas = 1
    if(pruebas == 0):

        numero_variables = 18
        listaVariables = crear_lista_variables(numero_variables,2)  
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

    if(pruebas == 1):

        fila1_num = 2
        fila2_num = 16
        var = crear_lista_variables(fila1_num + fila2_num,2)
        tiempos_orden_bueno = []
        tiempos_orden_malo = []
        for n in range(3,fila2_num + 1):

            fila1 = var[:fila1_num]
            fila2 = var[fila1_num:fila1_num + n]

            lista_factores_aux = crear_lista_factores_prueba_orden(fila1,fila2)

            numerator_orden = fila2[1:fila2_num - 1]
            numerator_orden.extend(fila1)

            denominator_order = fila2[fila2_num - 1:]

            '''
                print("Orden numerador")
                for var in numerator_orden:
                    print(var.get_name())

                print("-----------------------------")     
                print("Orden denominador")
                print(denominator_order[0].get_name())
            '''

            start_time = time.time()
            inferencia_condicional_itertools(lista_factores_aux,numerator_orden,denominator_order)
            total_time = time.time() - start_time
            tiempos_orden_bueno.append(total_time)
            
            '''print("-----------------------------")   
            print(f"Tiempo con orden bueno: {total_time}") '''  
            print("------------------------------")
            
        
            numerator_orden.reverse()

            start_time = time.time()
            inferencia_condicional_itertools(lista_factores_aux,numerator_orden,denominator_order)
            total_time = time.time() - start_time
            tiempos_orden_malo.append(total_time)

            
            print(f"Variables {fila1_num + n}: {total_time} ")   
            

        n_values = list(range(3, fila2_num + 1))

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(n_values, tiempos_orden_bueno, label="Orden bueno", color='blue')
        ax1.set_ylabel("Tiempo bueno (s)")
        ax1.legend()
        ax1.grid(True)

        ax2.plot(n_values, tiempos_orden_malo, label="Orden malo", color='red')
        ax2.set_xlabel("Número de variables en fila2")
        ax2.set_ylabel("Tiempo malo (s)")
        ax2.legend()
        ax2.grid(True)

        plt.show()