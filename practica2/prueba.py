import numpy 

"""
Clase Variable
name: string que indica el nombre de la variable, por ejemplo "A"
cardinality: entero que indica la cardinalidad de la variable.
values: retorna una lista de tuplas de las posibles combinaciones. Por ejemplo
        para cardinality = 3, retornará [("A",0),("A",1),("A",2)]
"""
class Variable:

    def __init__(self,name,cardinality):
        self.name = name
        self.cardinality = cardinality
        self.values = set()
        for i in range(0,cardinality):
            self.values.add((name,i))

    def get_name(self):
        return self.name

    def get_values(self):
        return self.values
    
    def get_cardinality(self):
        return self.cardinality
    

"""
Clase factor. Se emplea un mapa donde:
- Las llaves son conjuntos. Cada conjunto representa una asignación
  conjunta de variables, por ejemplo a0 b1 c0. Cada instancia
  queda representada como una tupla, por ejemplo ("A",0),("B",1),("C",0)
  Por lo tanto, una llave puede ser por ejemplo:
  frozenset({("A",0),("B",1),("C",0)}) representando a0 b1 c0.
- El valor es el valor flotante de la asignación. Por ejemplo 0.06.
"""
class Factor:
    """
    Crea un factor. Puede tener una asignación ya existente
    o comenzar vacío. También vamos a tener un set que simplemente
    contiene las variables que para la multiplicación será útil.
    """
    def __init__(self,asignaciones=None):
        if asignaciones:
            self.asignaciones = asignaciones
        else:
            self.asignaciones = {}
    
    def add_new_asignacion(self,fila,valor):
        self.asignaciones[fila] = valor

    def add_to_asignacion(self,fila,valor):
        self.asignaciones[fila] += valor

    def get_value(self,fila):
        return self.asignaciones[fila]

    def get_asignaciones(self):
        return self.asignaciones
    
    def get_variables(self):
        # Tomamos una fila cualquiera
        # Por ejemplo:
        # {("A",0),("B",0),("C",0)} obtenemos {"A","B","C"}
        random_asignacion = next(iter(self.asignaciones.keys()))
        variables = set()
        for ele in random_asignacion: #O(m)
            variables.add(ele[0]) 
        return variables

    def show_factor(self):
        print(self.asignaciones)

    
"""
Aplica la marginalización de una variable dada a un factor.
"""
def marginalize(factor,variable):
    variable_values = variable.get_values()                         #ejemplo: {("B",0),("B",1)}
    tau = Factor()
    for asignacion in factor.get_asignaciones().keys():             #ejemplo: {("A",0),("B",0),("C",0)}
        new_asignacion = frozenset(asignacion - variable_values)    #ejemplo: {("A",0),("C",0)}
        # A partir de aqui comprobamos el mapa del nuevo factor. Si por ejemplo {("A",0),("C",0)}
        # no estaba, se anhade con el valor de {("A",0),("B",0),("C",0)}. Si ya existe {("A",0),("C",0)},
        # significa que ya se anhadió el valor de {("A",0),("B",0),("C",0)} previamente y el de ahora se trata de
        # una nueva asignación, por ejemplo {("A",0),("B",1),("C",0)}, por lo que sumamos el valor al ya existente.
        if new_asignacion not in tau.get_asignaciones():
            tau.add_new_asignacion(new_asignacion,factor.get_value(asignacion))
        else:
            tau.add_to_asignacion(new_asignacion,factor.get_value(asignacion))
    return tau
        # n = numero de filas.
        # m = numero de tuplas de cada fila. Si aumenta m, también aumenta n.
        # Tenemos el for de cada fila, O(n)
        # Por cada fila hay operaciones de mapas O(1) y la operacion
        # new_asignacion = frozenset(asignacion - variable_values).
        # Esta operación consiste en iterar sobre cada elemento en asignacion y comprobar
        # si está en variable_values. Si no está ahí, lo anhade y si sí está no lo anhade.
        # Supuestamente el comprobar si está en variable_values es O(1). Se itera sobre asignacion,
        # luego O(m*1) = O(m)
        # Complejidad O(n*m), pero a medida que crecen:
        # n = 8, m = 3
        # n = 15, m = 4
        # n = 31, m = 5
        # Además esto es asumiendo cardinalidad de 2, pero si aumenta la cardinalidad
        # se aumenta aun más n y mientras m sigue igual.
        # n >> m, se puede considerar lineal O(n)

def factor_product(factor1,factor2):
    variables_factor1 = factor1.get_variables() #O(m) =aprox O(1)          #ej {"A","B","C"}
    variables_factor2 = factor2.get_variables() #O(m) =aprox O(1)          #ej {"B","C","D"}
    variables_comunes = variables_factor1.intersection(variables_factor2)  #ej {"B","C"}
    asignaciones_factor1 = factor1.get_asignaciones().keys()
    asignaciones_factor2 = factor2.get_asignaciones().keys()
    tao = Factor()
    for asignacion1 in asignaciones_factor1:                               #ej {("A",0),("B,0"),"("C,0")"}
        for asignacion2 in asignaciones_factor2:                           #ej {("B",1),("C,0"),"("D,0")"}
            en_comun = asignacion1.intersection(asignacion2)               #Solo se pueden multiplicar si tanto B como C tienen la misma asignacion
            variables_interseccion = set()                                 #Como uno tiene ("B,0") y el otro ("B",1) no se puede.
            for ele in en_comun:                                           #Obtenemos {("C",0)} -> {"C"} != variables_comunes = {"B","C"}
                variables_interseccion.add(ele[0])                         #Si el segundo hubiese sido {("B",0),("C,0"),"("D,0")"} la interseccion
            if (variables_interseccion == variables_comunes):              #es {("B",0),("C",0)"} -> {"B","C"} = variables_comunes
                new_asignacion = asignacion1.union(asignacion2)
                valor = factor1.get_value(asignacion1) * factor2.get_value(asignacion2)
                tao.add_new_asignacion(new_asignacion,valor)
    return tao
                                                                           
            

            



A = Variable("A",2)
B = Variable("B",2)
C = Variable("C",2)
valores = [0.01,0.02,0.06,0.08,0.03,0.06,0.12,0.16]
asignaciones = {}
i = 0
for a in range(0,A.get_cardinality()):
    for b in range(0,B.get_cardinality()):
        for c in range(0,C.get_cardinality()):
            key = frozenset({(A.get_name(), a),(B.get_name(), b),(C.get_name(), c)})
            asignaciones[key] = valores[i]
            i += 1

print("-------------------------------------")
print("Factor phi1:")
phi1 = Factor(asignaciones)
phi1.show_factor()
print("-------------------------------------")
print("Aplicamos marginalización sobre phi1:")
print(f"Variable a marginalizar: {B.get_name()}")
print("Factor tao1:")
tau1 = marginalize(phi1,B)
tau1.show_factor()
print("-------------------------------------")

A = Variable("A",2)
B = Variable("B",2)
C = Variable("C",2)
valores = [0.1,0.2,0.3,0.4]
asignaciones1 = {}
asignaciones2 = {}
i = 0
for a in range(0,A.get_cardinality()):
    for b in range(0,B.get_cardinality()):
        key = frozenset({(A.get_name(), a),(B.get_name(), b)})
        asignaciones1[key] = valores[i]
        i += 1
i = 0
for b in range(0,B.get_cardinality()):
    for c in range(0,C.get_cardinality()):
        key = frozenset({(B.get_name(), b),(C.get_name(), c)})
        asignaciones2[key] = valores[i]
        i += 1
print("Factor phi1:")
phi1 = Factor(asignaciones1)
phi1.show_factor()
print("Factor phi2:")
phi2 = Factor(asignaciones2)
phi2.show_factor()
print("Producto:")
factor_product(phi1,phi2).show_factor()


