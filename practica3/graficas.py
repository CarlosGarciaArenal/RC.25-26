from creacion_aleatoria import *
from chow_liu import *
import time

if __name__ == "__main__":

    num_variables  = 1005
    max_cardinalidad = 5
    lista_num = range(5, num_variables, 50)

    tiempos = [0] * len(lista_num)

    num_pasadas = 1
    for i in range(0,num_pasadas):

        print(f"\n\n----Pasada {i} -----")

        variables = crear_variables(num_variables,max_cardinalidad)
        tablas = crear_tabla(variables)
        
        for num_var in range(0,len(lista_num)):

            sub_lista = variables[:lista_num[num_var]]

            start = time.time()
            pesos = obtener_pesos(sub_lista, tablas)
            
        
            grafo = obtener_arbol_conjuntos(pesos, sub_lista)

            
            dir_arbol = asignar_direccionalidad(grafo)
            tiempos[num_var] +=time.time() - start

            print(f"Tiempo con {lista_num[num_var]}: {tiempos[num_var]}")
            


    tiempos = [tiempo / num_pasadas for tiempo in tiempos]

    plt.plot(lista_num, tiempos, marker="o", label="Chow-Liu")
    plt.title("Complejidad Empírica")
    plt.xlabel("Número de variables")
    plt.ylabel("Tiempo (segundos)")
    plt.legend()
    plt.grid(True)
    plt.show()